"""
GutenaAPI
=========
This module contains the Flask app and query_books method will be invoked
for the API to process the request and povide a response in JSON format.
"""

# imports
import traceback

from flask import Flask, jsonify, request

from gutenapi.gutendb import get_books

app = Flask(__name__)


@app.route("/api", methods=["GET", "POST"])
def query_books():
    """This method will be invoked for the API to process the request
    and povide a response in JSON format"""

    try:
        # Get input parameters when request method is POST
        if request.method == "POST":
            request_json = request.get_json()
            guten_ids = request_json.get("guten_ids", None)
            languages = request_json.get("languages", None)
            topics = request_json.get("topics", None)
            authors = request_json.get("authors", None)
            titles = request_json.get("titles", None)
            mime_types = request_json.get("mime_types", None)
            page = request_json.get("page", 0)

        # Get input parameters when request method is GET
        if request.method == "GET":
            guten_ids = request.args.get("guten_ids", None)
            if guten_ids is not None:
                guten_ids = guten_ids.split(",")
            languages = request.args.get("languages", None)
            if languages is not None:
                languages = languages.split(",")
            topics = request.args.get("topics", None)
            if topics is not None:
                topics = topics.split(",")
            authors = request.args.get("authors", None)
            if authors is not None:
                authors = authors.split(",")
            titles = request.args.get("titles", None)
            if titles is not None:
                titles = titles.split(",")
            mime_types = request.args.get("mime_types", None)
            if mime_types is not None:
                mime_types = mime_types.split(",")
            page = request.args.get("page", 0)

        # Call get_books method to obtain the response data
        response = get_books(
            guten_ids=guten_ids,
            languages=languages,
            topics=topics,
            authors=authors,
            titles=titles,
            mime_types=mime_types,
            page=int(page),
        )
    except:
        text_error = traceback.format_exc()
        response = {"type": "error", "details": text_error}

    # return response in JSON format
    return jsonify(response)
