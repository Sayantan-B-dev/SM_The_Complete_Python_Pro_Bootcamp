"""
Cafe & Wifi REST API
Provides data about remote-work-friendly cafes in London.
Endpoints:
- GET  /random       : random cafe
- GET  /all          : all cafes
- GET  /search?loc=... : cafes by location
- POST /add          : add new cafe (form or JSON)
- PATCH /update-price/<cafe_id> : update coffee price
- DELETE /report-closed/<cafe_id> : delete cafe (requires API key)
- GET  /             : serves frontend (index.html)
"""

import os
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

# -------------------------------------------------------------------
# Initialize Flask app and database
# -------------------------------------------------------------------
app = Flask(__name__)

# Database configuration – SQLite file will be created in 'instance' folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -------------------------------------------------------------------
# Load API key from environment variable (for DELETE endpoint)
# In production, set this variable. For development, a default is provided.
# Create a .env file or set environment variable API_KEY.
# -------------------------------------------------------------------
API_KEY = os.environ.get('API_KEY')

# -------------------------------------------------------------------
# Cafe Model
# -------------------------------------------------------------------
class Cafe(db.Model):
    __tablename__ = 'cafe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        """
        Convert model instance to dictionary for JSON serialization.
        Uses introspection to get all column names and values.
        """
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# -------------------------------------------------------------------
# Helper function to convert string to boolean (for POST)
# -------------------------------------------------------------------
def str_to_bool(value):
    """Convert string or bool to Python bool. Raises ValueError if invalid."""
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    lower_val = str(value).lower().strip()
    if lower_val in ('true', '1', 'yes', 'on'):
        return True
    if lower_val in ('false', '0', 'no', 'off'):
        return False
    raise ValueError(f"Invalid boolean value: {value}")

# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------

@app.route('/')
def home():
    """Serve the minimal frontend UI."""
    return render_template('index.html')


@app.route('/random', methods=['GET'])
def get_random_cafe():
    """Return a random cafe."""
    cafe = Cafe.query.order_by(func.random()).first()
    if cafe:
        return jsonify(cafe.to_dict())
    else:
        return jsonify({"error": "No cafes found in database"}), 404


@app.route('/all', methods=['GET'])
def get_all_cafes():
    """Return all cafes as a JSON array."""
    cafes = Cafe.query.all()
    return jsonify([cafe.to_dict() for cafe in cafes])


@app.route('/search', methods=['GET'])
def search_cafe():
    """Return cafes matching the location query parameter 'loc'."""
    location = request.args.get('loc')
    if not location or location.strip() == '':
        return jsonify({"error": "Missing 'loc' query parameter."}), 400

    # Case‑insensitive exact match (you could also use ilike for partial)
    cafes = Cafe.query.filter(func.lower(Cafe.location) == func.lower(location)).all()
    if cafes:
        return jsonify([cafe.to_dict() for cafe in cafes])
    else:
        return jsonify({"error": "No cafes found in that location."}), 404


@app.route('/add', methods=['POST'])
def add_cafe():
    """
    Add a new cafe.
    Accepts application/x-www-form-urlencoded or JSON.
    Required fields: name, map_url, img_url, location,
                     has_sockets, has_toilet, has_wifi, can_take_calls, seats.
    Optional: coffee_price.
    """
    # Parse request data
    data = request.get_json()
    if not data:
        data = request.form

    # Check required fields
    required_fields = ['name', 'map_url', 'img_url', 'location',
                       'has_sockets', 'has_toilet', 'has_wifi',
                       'can_take_calls', 'seats']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Convert boolean fields
    try:
        has_sockets = str_to_bool(data['has_sockets'])
        has_toilet = str_to_bool(data['has_toilet'])
        has_wifi = str_to_bool(data['has_wifi'])
        can_take_calls = str_to_bool(data['can_take_calls'])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Create new cafe
    new_cafe = Cafe(
        name=data['name'],
        map_url=data['map_url'],
        img_url=data['img_url'],
        location=data['location'],
        has_sockets=has_sockets,
        has_toilet=has_toilet,
        has_wifi=has_wifi,
        can_take_calls=can_take_calls,
        seats=data['seats'],
        coffee_price=data.get('coffee_price')  # may be None
    )

    try:
        db.session.add(new_cafe)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    return jsonify(new_cafe.to_dict()), 201


@app.route('/update-price/<int:cafe_id>', methods=['PATCH'])
def update_price(cafe_id):
    """Update the coffee_price of a specific cafe."""
    cafe = db.session.get(Cafe, cafe_id)
    if not cafe:
        return jsonify({"error": "Cafe with that id not found."}), 404

    data = request.get_json()
    if not data:
        data = request.form

    new_price = data.get('coffee_price')
    if not new_price:
        return jsonify({"error": "Missing field: coffee_price"}), 400

    try:
        cafe.coffee_price = new_price
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    return jsonify({"success": "Successfully updated the price."}), 200


@app.route('/report-closed/<int:cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    """Delete a cafe. Requires valid api-key query parameter."""
    provided_key = request.args.get('api-key')
    if provided_key != API_KEY:
        return jsonify({"error": "You are not authorized to delete. Please provide the correct api-key."}), 403

    cafe = db.session.get(Cafe, cafe_id)
    if not cafe:
        return jsonify({"error": "Cafe with that id not found."}), 404

    try:
        db.session.delete(cafe)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    return jsonify({"success": "Cafe deleted successfully."}), 200


# -------------------------------------------------------------------
# Run the application
# -------------------------------------------------------------------
if __name__ == '__main__':
    # Ensure tables exist (the provided database already has them, but this is safe)
    with app.app_context():
        db.create_all()
    app.run(debug=True)