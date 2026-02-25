from flask import Flask, render_template, jsonify
import pandas as pd
import analyze_launches as al   # import with alias
import analyze_rockets as ar
import os

app = Flask(__name__)

def load_launches():
    if os.path.exists('data/launches.csv'):
        return pd.read_csv('data/launches.csv').to_dict(orient='records')
    return []

def load_rockets():
    if os.path.exists('data/rockets.csv'):
        return pd.read_csv('data/rockets.csv').to_dict(orient='records')
    return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/launches')
def launches():
    data = load_launches()
    return render_template('launches.html', launches=data)

@app.route('/rockets')
def rockets():
    data = load_rockets()
    return render_template('rockets.html', rockets=data)

# Renamed route functions to avoid shadowing imports
@app.route('/analyze/launches')
def launch_analysis():
    stats = al.get_launch_stats()
    return render_template('analyze_launches.html', stats=stats)

@app.route('/analyze/rockets')
def rocket_analysis():
    stats = ar.get_rocket_stats()
    return render_template('analyze_rockets.html', stats=stats)

# API endpoints (optional)
@app.route('/api/launch_stats')
def launch_stats_api():
    return jsonify(al.get_launch_stats())

@app.route('/api/rocket_stats')
def rocket_stats_api():
    return jsonify(ar.get_rocket_stats())

if __name__ == '__main__':
    app.run(debug=True)