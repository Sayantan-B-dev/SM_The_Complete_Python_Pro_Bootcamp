# Top 10 Movies Website

A Flask web application that lets users create and manage a personal list of top movies. Movies are automatically ranked based on user ratings. Data is stored in SQLite, and new movies can be added by searching The Movie Database (TMDB) API.

## Technologies Used and Where

- **Flask** – Core web framework. Handles routing, request/response cycle, and template rendering.
- **Flask-SQLAlchemy** – ORM for database interactions. Defines the `Movie` model and provides session management.
- **SQLite** – Lightweight file‑based database. Stores movie data in `instance/movies.db`.
- **WTForms (Flask-WTF)** – Form handling and validation. Used for the add form (`FindMovieForm`) and edit form (`RateMovieForm`).
- **Bootstrap-Flask** – Simplifies rendering Bootstrap‑styled forms. Used in `add.html` and `edit.html` with the `render_form` macro.
- **Requests** – Makes HTTP calls to the TMDB API for movie search and details.
- **CSRF Protection** – Flask-WTF provides CSRF tokens for all forms, including the delete button.
- **Jinja2** – Templating engine. Used to loop through movies and display data dynamically.
- **python-dotenv** (optional) – Can be used to load the TMDB API key and secret key from a `.env` file.

## Setup Instructions

1. **Clone or download** this project.
2. **Create a virtual environment** and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. **Obtain a TMDB API Key**:
   - Register at [themoviedb.org](https://www.themoviedb.org/).
   - Go to Settings → API → Create (or request) an API key (v3 auth). Copy the **API Key** (not the read access token).
4. **Set your API key**:
   - **Option A (Environment Variable – Recommended)**:  
     Set an environment variable named `TMDB_API_KEY` with your key.  
     - On Windows (Command Prompt): `set TMDB_API_KEY=your_key_here`  
     - On Windows (PowerShell): `$env:TMDB_API_KEY="your_key_here"`  
     - On macOS/Linux: `export TMDB_API_KEY=your_key_here`  
   - **Option B (Hardcode – for testing only)**:  
     Open `main.py` and replace `'your_tmdb_api_key_here'` with your actual key.  
     **Warning:** Avoid committing this change if you use version control.
5. **Run the application**:
   ```bash
   python main.py
   ```
6. **Open** `http://127.0.0.1:5000/` in your browser.

## Features

- **View Movies** – All movies are displayed as cards with title, year, description, poster, rating, review, and ranking.
- **Edit** – Click “Edit” to update a movie’s rating and personal review.
- **Delete** – Click “Delete” (POST request with CSRF protection) to remove a movie.
- **Add New Movie** – Enter a title; the app searches TMDB and lets you select the correct film. Full details (title, year, poster, description) are fetched and stored. You are then redirected to the edit page to add a rating and review.
- **Automatic Ranking** – Every time the home page loads, all movies are sorted by rating and assigned a rank (1 = highest rating). Unrated movies show “None” and do not affect ranking.

## File Structure

```
top10movies/
├── main.py                 # Application entry point, routes, and database model
├── forms.py                # WTForms classes
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── templates/              # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── add.html
│   ├── edit.html
│   └── select.html
└── static/
    └── css/
        └── styles.css      # Optional custom styles
```

## Notes

- The `instance/` folder (containing `movies.db`) is created automatically on first run.
- Movie titles are unique – duplicate entries are prevented.
- All database modifications (add, edit, delete) are committed immediately and persisted.
- CSRF protection is enabled for all forms; the delete button uses a hidden CSRF token.
- Error handling is minimal; feel free to enhance with try/except blocks and user feedback.

## Using Your Provided API Key

You provided:

- **API Key:** `b30************************5ca`  
- **Read Access Token:** `ey******************GdsVgHKK04`

The project uses the **API Key** (v3 auth) for all TMDB requests. Replace the placeholder in the code or set the environment variable `TMDB_API_KEY` to this value. Do **not** share your key publicly.

## Future Improvements

- Add user authentication to support multiple users.
- Allow sorting by other criteria (year, title).
- Implement a “watched” flag or multiple lists.
- Use environment variables more securely with `python-dotenv` and a `.env` file.

---
Enjoy building your movie list!