# Cafe & Wifi API – Remote Work Friendly Cafes

A RESTful API and minimal frontend that provides curated data about cafes in London suitable for remote work. The API allows developers to access cafe details, and the frontend offers a user-friendly interface to browse, filter, and discover cafes.

## Features

- **RESTful API** with full CRUD operations
- **SQLite database** with pre-populated cafe data
- **JSON responses** for easy integration
- **Authentication** via API key for DELETE operations
- **Minimal frontend** with black/white theme, rounded borders, and padding
- **Filtering** by location and amenities (sockets, toilet, Wi-Fi, calls allowed)
- **Random cafe** selector

## Tech Stack

- **Backend**: Python 3.13, Flask, Flask-SQLAlchemy
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Tools**: Postman (for testing and documentation)

## Project Structure

```
cafe-api/
├── instance/
│   └── cafes.db                # SQLite database (provided)
├── static/
│   └── style.css                # Frontend styling
├── templates/
│   └── index.html               # Frontend UI
├── main.py                       # Flask application with all endpoints
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Setup & Installation

### Prerequisites
- Python 3.13 or higher
- pip (Python package manager)
- Git (optional)

### Step 1: Clone or download the repository
```bash
git clone <repository-url>
cd cafe-api
```

### Step 2: Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set up the database
Place the provided `cafes.db` file inside the `instance/` folder. If you don't have it, the application will create an empty database on first run, but you'll need to populate it manually or use the original.

### Step 5: (Optional) Configure API key
The DELETE endpoint requires an API key. By default, the code uses `TopSecretAPIKey`. You can override it by setting the environment variable `API_KEY`:

**macOS/Linux:**
```bash
export API_KEY="YourSecretKey"
```
**Windows (Command Prompt):**
```cmd
set API_KEY=YourSecretKey
```
**Windows (PowerShell):**
```powershell
$env:API_KEY="YourSecretKey"
```

### Step 6: Run the application
```bash
python main.py
```

The server will start at `http://127.0.0.1:5000`. Open this URL in your browser to see the frontend.

## API Documentation

All endpoints return JSON. The base URL is `http://127.0.0.1:5000`.

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/random` | Returns a random cafe | None |
| GET | `/all` | Returns all cafes | None |
| GET | `/search` | Search cafes by location | `loc` (query, required) |
| POST | `/add` | Add a new cafe | Body: form-urlencoded or JSON with fields below |
| PATCH | `/update-price/<cafe_id>` | Update coffee price | Body: `coffee_price` |
| DELETE | `/report-closed/<cafe_id>` | Delete a cafe | Query: `api-key` (required) |

### Required fields for POST `/add`
- `name` (string)
- `map_url` (string)
- `img_url` (string)
- `location` (string)
- `has_sockets` (boolean: true/false or 1/0)
- `has_toilet` (boolean)
- `has_wifi` (boolean)
- `can_take_calls` (boolean)
- `seats` (string)
- `coffee_price` (string, optional)

### Example Requests

**GET /random**
```bash
curl http://127.0.0.1:5000/random
```

**GET /search?loc=Shoreditch**
```bash
curl "http://127.0.0.1:5000/search?loc=Shoreditch"
```

**POST /add** (JSON)
```bash
curl -X POST http://127.0.0.1:5000/add \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Cafe",
    "map_url": "https://goo.gl/maps/...",
    "img_url": "https://example.com/photo.jpg",
    "location": "Soho",
    "has_sockets": true,
    "has_toilet": false,
    "has_wifi": true,
    "can_take_calls": true,
    "seats": "20-30",
    "coffee_price": "£3.50"
  }'
```

**PATCH /update-price/1** (form)
```bash
curl -X PATCH http://127.0.0.1:5000/update-price/1 \
  -d "coffee_price=£4.00"
```

**DELETE /report-closed/1?api-key=TopSecretAPIKey**
```bash
curl -X DELETE "http://127.0.0.1:5000/report-closed/1?api-key=TopSecretAPIKey"
```

## Frontend Usage

The frontend (`index.html`) is served at the root URL (`/`). It provides:

- **Cafe grid**: Displays all cafes with photo, location, price, seats, amenities, and a "View on Google Maps" link.
- **Filter panel**: Filter by location (dropdown populated from data) and amenities (checkboxes). Click "Apply Filters" to update the grid.
- **Reset button**: Clears all filters and shows all cafes.
- **Random cafe button**: Fetches a random cafe from the API and displays it alone.

All filtering is done client‑side after fetching all cafes once. The random button calls the `/random` endpoint separately.

## Code Explanation

### `main.py` – Key Functions

- **`to_dict(self)`**: Converts a `Cafe` model instance to a dictionary for JSON serialization. Uses SQLAlchemy introspection to include all columns.
- **`str_to_bool(value)`**: Helper to convert string or boolean input to Python bool. Raises `ValueError` for invalid values.
- **`get_random_cafe()`**: Queries a random cafe using `func.random()`.
- **`get_all_cafes()`**: Returns all cafes as a JSON array.
- **`search_cafe()`**: Filters cafes by location (case‑insensitive exact match). Returns 404 if none found.
- **`add_cafe()`**: Handles POST requests. Validates required fields, converts booleans, and adds a new record.
- **`update_price(cafe_id)`**: Updates only the `coffee_price` field of a specific cafe.
- **`delete_cafe(cafe_id)`**: Deletes a cafe after verifying the API key. Returns 403 for invalid key, 404 if cafe not found.
- **`home()`**: Renders the `index.html` template.

### Frontend JavaScript (`index.html`)

- **`loadAllCafes()`**: Fetches all cafes from `/all`, stores them in `allCafes`, renders them, and populates the location dropdown.
- **`populateLocationDropdown(cafes)`**: Extracts unique locations and fills the `<select>` element.
- **`applyFilters()`**: Filters `allCafes` based on selected location and checked amenities, then re‑renders.
- **`resetFilters()`**: Clears filter selections and shows all cafes.
- **`loadRandomCafe()`**: Fetches a random cafe from `/random` and renders it alone.
- **`renderCafes(cafes)`**: Generates HTML for each cafe card using the exact style defined in `style.css`.

### CSS (`style.css`)

- Defines black background, white text, rounded borders, and padding.
- Styles the cafe cards, images, amenities, map link, filter panel, and buttons.
- No emojis are used; all labels are plain text.

## Environment Variables

- `API_KEY`: Secret key for DELETE endpoint. If not set, defaults to `TopSecretAPIKey` (for development only). In production, always set this variable.

## Testing with Postman

A Postman collection is available in the repository (if included). You can import it to test all endpoints. The collection includes:
- Get Random Cafe
- Get All Cafes
- Search by Location
- Add New Cafe
- Update Coffee Price
- Delete Cafe (with API key)

## License

This project is for educational purposes as part of a Python course. Feel free to use and modify it.

## Author

Sayantan-b-dev

---

For any issues or questions, please open an issue on the repository.