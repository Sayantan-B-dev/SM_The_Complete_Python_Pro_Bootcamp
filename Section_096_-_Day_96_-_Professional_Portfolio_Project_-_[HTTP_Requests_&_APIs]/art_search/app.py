import os
import time
from flask import Flask, render_template, request, jsonify, url_for, redirect
import requests

app = Flask(__name__)

# Custom Jinja filter to exclude keys from a dictionary
@app.template_filter('exclude')
def exclude_dict(d, *keys):
    return {k: v for k, v in d.items() if k not in keys}

API_KEY = os.environ.get('ARTSEARCH_API_KEY')
BASE_URL = 'https://api.artsearch.io/artworks'

TYPES = [
    "tapestry", "collotype", "collage", "printmaking", "cutting", "digital_art",
    "sculpture", "metalwork", "fragment", "token", "embroidery", "painting",
    "jewellery", "print", "ornament", "photograph", "statuette", "furniture",
    "needlework", "drawing", "miniature", "tile", "stereograph", "calligraphy"
]

MATERIALS = [
    "ferrous_lactate", "ink", "textile", "metal", "bronze", "canvas", "stone",
    "reduced_iron", "horn", "stoneware", "in_shell_walnuts", "chalk", "velvet",
    "silver", "charcoal", "gold_leaf", "candied_walnuts", "porcelain",
    "walnut_halves", "jade", "cotton", "paint", "ferrous_fumarate", "graphite",
    "cobalt", "sandstone", "plastic", "walnut_pieces", "clay", "walnuts",
    "cupric_sulfate", "ivory", "ferric_orthophosphate", "earthenware", "tin",
    "pen", "linen", "mahogany", "electrolytic_iron", "silk", "crayon",
    "black_walnuts", "brush", "beech_wood", "terracotta", "glass", "lead",
    "brass", "oil_paint", "pencil", "leather", "gold", "marble", "watercolor",
    "diamond", "iron", "ferrous_sulfate", "walnut_halves_and_pieces", "gouache",
    "wool", "ceramic", "parchment", "cork", "limestone", "copper_gluconate",
    "paper", "pastel", "copper", "cardboard", "plant_material", "oak", "wood"
]

TECHNIQUES = [
    "engraving", "grinding", "embroidering", "etching", "vitrification",
    "gilding", "lithography", "knitting", "cyanotype", "silkscreen", "woodcut",
    "printing", "drypoint", "photolithography", "weaving", "sawing", "casting",
    "glassblowing", "block_printing", "photographing", "forging"
]

def call_api(endpoint, params=None):
    if params is None:
        params = {}
    params['api-key'] = API_KEY
    url = f"{BASE_URL}{endpoint}"
    try:
        # time.sleep(0.5)  # simulate slow loading (remove in production)
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {'error': 'The server is taking too long to respond. Please try again later.'}
    except requests.exceptions.ConnectionError:
        return {'error': 'Unable to connect to the art database. Please check your internet connection.'}
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        if status_code == 401:
            return {'error': 'Invalid API Key. Please check your configuration.'}
        elif status_code == 404:
            return {'error': 'The requested artwork or resource was not found.'}
        elif status_code == 429:
            return {'error': 'Too many requests. Please slow down.'}
        return {'error': f'Server error: {status_code}. Please try again later.'}
    except requests.exceptions.RequestException as e:
        return {'error': 'An unexpected error occurred while fetching art data.'}

@app.route('/')
def index():
    return render_template('index.html', types=TYPES, materials=MATERIALS, techniques=TECHNIQUES)

@app.route('/search')
def search():
    query = request.args.get('query', '')
    number = request.args.get('number', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    filters = {
        'type': request.args.get('type'),
        'material': request.args.get('material'),
        'technique': request.args.get('technique'),
        'origin': request.args.get('origin'),
        'earliest-start-date': request.args.get('earliest_start'),
        'latest-start-date': request.args.get('latest_start'),
        'min-ratio': request.args.get('min_ratio', type=float),
        'max-ratio': request.args.get('max_ratio', type=float),
    }
    params = {'query': query, 'number': number, 'offset': offset}
    params.update({k: v for k, v in filters.items() if v not in (None, '')})

    data = call_api('', params=params)

    if 'error' in data:
        return render_template('error.html', error=data['error'])

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('_results.html',
                               artworks=data.get('artworks', []),
                               total=data.get('available', 0),
                               query=query,
                               number=number,
                               offset=offset)
    return render_template('index.html',
                           artworks=data.get('artworks', []),
                           total=data.get('available', 0),
                           query=query,
                           number=number,
                           offset=offset,
                           types=TYPES, materials=MATERIALS, techniques=TECHNIQUES)

@app.route('/artwork/<int:id>')
def artwork_detail(id):
    data = call_api(f'/{id}')
    if 'error' in data:
        return render_template('error.html', error=data['error'])
    return render_template('artwork.html', artwork=data)

@app.route('/random')
def random_artwork():
    data = call_api('/random')
    if 'error' in data:
        return render_template('error.html', error=data['error'])
    return redirect(url_for('artwork_detail', id=data['id']))

if __name__ == '__main__':
    app.run(debug=True)