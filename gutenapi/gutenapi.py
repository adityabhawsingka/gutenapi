from flask import Flask, jsonify, request
from gutenapi.gutendb import get_books

app = Flask(__name__)


@app.route("/api", methods=["GET", "POST"])
def query_books():

    if request.method == "POST":
        request_json = request.get_json()
        guten_ids = request_json.get("guten_ids", None)
        book_langs = request_json.get("book_langs", None)
        topics = request_json.get("topics", None)
        authors = request_json.get("authors", None)
        titles = request_json.get("titles", None)
        mime_types = request_json.get("mime_types", None)
        page = request_json.get("page", 0)

    if request.method == "GET":
        guten_ids = request.args.get("guten_ids", None)
        if guten_ids is not None:
            guten_ids = list(guten_ids)
        book_langs = request.args.get("book_langs", None)
        if book_langs is not None:
            book_langs = book_langs.split(",")
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

    books = get_books(
        guten_ids=guten_ids,
        book_langs=book_langs,
        topics=topics,
        authors=authors,
        titles=titles,
        mime_types=mime_types,
        page=int(page)
    )

    return jsonify(books)

