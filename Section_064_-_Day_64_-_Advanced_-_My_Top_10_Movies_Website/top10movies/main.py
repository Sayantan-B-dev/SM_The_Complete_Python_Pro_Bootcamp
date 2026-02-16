import os
import time
import requests
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap5
from forms import RateMovieForm, FindMovieForm
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, Timeout

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '8BYkEfBA6O6donzWlSihBXox7C0sKR6b')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bootstrap = Bootstrap5(app)

# ----------------------------------------------------------------------
# TMDB API Configuration – with fallback: token first, then API key
# ----------------------------------------------------------------------
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
TMDB_ACCESS_TOKEN = os.environ.get('TMDB_ACCESS_TOKEN')
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_DETAILS_URL = "https://api.themoviedb.org/3/movie"
TMDB_POPULAR_URL = "https://api.themoviedb.org/3/movie/popular"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def tmdb_request(url, params=None, retries=5):
    """
    Make a request to TMDB using Bearer token if available, otherwise API key.
    Retries up to `retries` times on connection errors or timeouts.
    Returns response object if successful, otherwise raises an exception.
    """
    headers = {}
    request_params = params.copy() if params else {}

    if TMDB_ACCESS_TOKEN:
        headers["Authorization"] = f"Bearer {TMDB_ACCESS_TOKEN}"
        print(f"Using Bearer token for {url}")
    elif TMDB_API_KEY:
        request_params["api_key"] = TMDB_API_KEY
        print(f"Using API key for {url}")
    else:
        raise Exception("No TMDB credentials found. Set TMDB_ACCESS_TOKEN or TMDB_API_KEY in .env")

    for attempt in range(1, retries + 1):
        try:
            print(f"Attempt {attempt} - Request params: {request_params}")
            response = requests.get(url, headers=headers, params=request_params, timeout=15)
            print(f"Response status: {response.status_code}")
            if response.status_code != 200:
                print(f"Response text: {response.text[:200]}")
            response.raise_for_status()
            return response
        except (ConnectionError, Timeout) as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt == retries:
                raise  # re-raise after final attempt
            wait = 2 ** attempt  # exponential backoff: 2,4,8,16,32 seconds
            print(f"Waiting {wait} seconds before retry...")
            time.sleep(wait)
        except Exception as e:
            # For other HTTP errors, don't retry
            raise

# ----------------------------------------------------------------------
# Database Model
# ----------------------------------------------------------------------
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'

with app.app_context():
    db.create_all()

# ----------------------------------------------------------------------
# Home Page
# ----------------------------------------------------------------------
@app.route("/")
def home():
    """Render home page with user's movies and popular movies section."""
    # User's personal movies (for the top list)
    user_movies = db.session.execute(
        db.select(Movie).order_by(Movie.rating.desc())
    ).scalars().all()

    # Assign rankings to user's movies
    rank = 1
    for movie in user_movies:
        if movie.rating is not None:
            movie.ranking = rank
            rank += 1
        else:
            movie.ranking = None
    db.session.commit()

    return render_template("index.html", movies=user_movies)

# ----------------------------------------------------------------------
# API endpoint to get popular movies (JSON)
# ----------------------------------------------------------------------
@app.route("/api/popular")
def popular_movies():
    """Return a JSON list of popular movies from TMDB."""
    page = request.args.get("page", 1, type=int)
    try:
        response = tmdb_request(TMDB_POPULAR_URL, {"page": page})
        data = response.json()
        # Simplify the response to only needed fields
        movies = []
        for item in data.get("results", []):
            movies.append({
                "id": item["id"],
                "title": item["title"],
                "poster": f"{TMDB_IMAGE_BASE_URL}{item['poster_path']}" if item.get("poster_path") else "https://via.placeholder.com/500x750?text=No+Poster",
                "year": item["release_date"][:4] if item.get("release_date") else "Unknown",
                "overview": item["overview"][:200] + "..." if item.get("overview") else "No description",
                "vote_average": item.get("vote_average", 0)
            })
        return jsonify({
            "movies": movies,
            "page": data.get("page"),
            "total_pages": data.get("total_pages")
        })
    except Exception as e:
        print(f"Error in /api/popular: {e}")
        return jsonify({"error": str(e)}), 500

# ----------------------------------------------------------------------
# Edit Movie
# ----------------------------------------------------------------------
@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    movie = db.get_or_404(Movie, movie_id)
    form = RateMovieForm(rating=movie.rating, review=movie.review)
    if form.validate_on_submit():
        movie.rating = form.rating.data
        movie.review = form.review.data
        db.session.commit()
        flash("Movie successfully updated!")
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)

# ----------------------------------------------------------------------
# Delete Movie
# ----------------------------------------------------------------------
@app.route("/delete/<int:movie_id>", methods=["POST"])
def delete(movie_id):
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("Movie deleted!")
    return redirect(url_for('home'))

# ----------------------------------------------------------------------
# Add Movie – Step 1: Search
# ----------------------------------------------------------------------
@app.route("/add", methods=["GET", "POST"])
def add():
    form = FindMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        try:
            response = tmdb_request(TMDB_SEARCH_URL, {"query": movie_title})
            data = response.json()
            results = data.get("results", [])
            if not results:
                flash("No movies found with that title. Please try again.")
                return render_template("add.html", form=form)
            return render_template("select.html", options=results)
        except Exception as e:
            print(f"Error in /add: {e}")
            flash("Network error – please check your internet connection and try again.")
            return render_template("add.html", form=form)
    return render_template("add.html", form=form)

# ----------------------------------------------------------------------
# Find Movie – Step 2: Get details and create entry
# ----------------------------------------------------------------------
@app.route("/find")
def find_movie():
    movie_id = request.args.get("id")
    if not movie_id:
        flash("No movie selected.")
        return redirect(url_for('add'))

    try:
        response = tmdb_request(f"{TMDB_DETAILS_URL}/{movie_id}", {"language": "en-US"})
        data = response.json()
    except Exception as e:
        print(f"🔥 ERROR in /find for movie_id {movie_id}: {e}")
        flash("Network error – please check your internet connection and try again.")
        return redirect(url_for('add'))

    title = data.get("title", "Unknown Title")
    release_date = data.get("release_date")
    year = release_date[:4] if release_date and len(release_date) >= 4 else "Unknown"
    poster_path = data.get("poster_path")
    if poster_path:
        img_url = f"{TMDB_IMAGE_BASE_URL}{poster_path}"
    else:
        img_url = "https://via.placeholder.com/500x750?text=No+Poster"
    description = data.get("overview", "No description available.")

    # Check for duplicate
    existing_movie = db.session.execute(
        db.select(Movie).where(Movie.title == title)
    ).scalar()
    if existing_movie:
        flash(f'"{title}" is already in your list.')
        return redirect(url_for('edit', movie_id=existing_movie.id))

    # Create new movie
    new_movie = Movie(
        title=title,
        year=year,
        description=description,
        rating=None,
        ranking=None,
        review=None,
        img_url=img_url
    )
    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for('edit', movie_id=new_movie.id))

if __name__ == "__main__":
    app.run(debug=True)