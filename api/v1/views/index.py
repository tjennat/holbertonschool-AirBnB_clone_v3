#!/usr/bin/python3
"""Defines a route for the Airbnb clone project's API status."""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def get_status():
    """ Endpoint to get the status of the Airbnb clone project's API."""
    return jsonify({"status": "OK"})


@app_views.route('stats')
def get_stats():
    """Retrieves the number of each object by type"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }

    return jsonify(stats)
