# gutenapi
Project Gutenberg API

This API is hosted publicly on Heroku, below are some sample calls to this API.

```
https://gutenapi.herokuapp.com/api?languages=en,fr&topics=child,infant
https://gutenapi.herokuapp.com/api?guten_ids=1
https://gutenapi.herokuapp.com/api?authors=jeff&page=3
```

### Parameters
Following filter params can be passed to the API:

| Parameter      | Description                                           |
| ------------- | -------------                                         |
| guten_ids     | List of book Gutenberg ids                            |
| languages     | List of book languages                                |
| authors       | List of book authors                                  |
| titles        | List of book titles                                   |
| topics        | List of book topics(Queried on booksjelf and subject) |
| mime_types    | List of mime_types(Queried on book format)            |

Other parameters:

| Parameter      | Description                                           |
| ------------- | -------------                                         |
| page     | Page number, should be 0 or not passed for the initial request. |



### Request Methods

API supports GET and POST methods.

Sample GET requests:

```
https://gutenapi.herokuapp.com/api?guten_ids=1,2
https://gutenapi.herokuapp.com/api?languages=en&authors=Jeff
https://gutenapi.herokuapp.com/api?languages=en&authors=Jeff&page=1
https://gutenapi.herokuapp.com/api?topics=child,infant
https://gutenapi.herokuapp.com/api?titles=independence,freedom
https://gutenapi.herokuapp.com/api?mime_types=ebook
```

Sample POST requests:

```
curl  https://gutenapi.herokuapp.com/api -d '{"guten_ids": [1,2]}' -H 'Content-Type: application/json'
curl  https://gutenapi.herokuapp.com/api -d '{"languages": ["en"], "authors": ["Jeff"]}' -H 'Content-Type: application/json'
curl  https://gutenapi.herokuapp.com/api -d '{"languages": ["en"], "authors": ["Jeff"], "page": 1}' -H 'Content-Type: application/json'
curl  https://gutenapi.herokuapp.com/api -d '{"topics": ["child","infant"]}' -H 'Content-Type: application/json'
curl  https://gutenapi.herokuapp.com/api -d '{"titles": ["independence","freedom"]}' -H 'Content-Type: application/json'
curl  https://gutenapi.herokuapp.com/api -d '{"mime_types": ["ebook"]}' -H 'Content-Type: application/json'
```


### Output

The API returns a JSON response.

Sucessful response:

```
{
  "books"   : <List of book objects>,
  "count"   : <number of matchig books>,
  "next"    : <next page number>,
  "previous": <previous page number>
 }
```

 Error response:
 
 ```
{
  "details": <error details>,
  "type"   : "error"
 }
```

#### Sample

https://gutenapi.herokuapp.com/api?guten_ids=1

 ```json
{
  "books": [
    {
      "authors": [
        {
          "birth_year": 1743,
          "death_year": 1826,
          "name": "Jefferson, Thomas"
        }
      ],
      "bookshelves": [
        "United States Law",
        "Politics",
        "American Revolutionary War"
      ],
      "download_count": 638,
      "gutenberg_id": 1,
      "languages": [
        "en"
      ],
      "links": [
        {
          "mime_type": "text/plain",
          "url": "http://www.gutenberg.org/ebooks/1.txt.utf-8"
        },
        {
          "mime_type": "application/prs.tex",
          "url": "http://www.gutenberg.org/6/5/2/6527/6527-t.zip"
        },
        {
          "mime_type": "application/epub+zip",
          "url": "http://www.gutenberg.org/ebooks/1.epub.images"
        },
        {
          "mime_type": "application/rdf+xml",
          "url": "http://www.gutenberg.org/ebooks/1.rdf"
        },
        {
          "mime_type": "text/plain; charset=us-ascii",
          "url": "http://www.gutenberg.org/files/1/1.txt"
        },
        {
          "mime_type": "application/x-mobipocket-ebook",
          "url": "http://www.gutenberg.org/ebooks/1.kindle.noimages"
        },
        {
          "mime_type": "text/html",
          "url": "http://www.gutenberg.org/ebooks/1.html.images"
        }
      ],
      "subjects": [
        "United States -- History -- Revolution, 1775-1783 -- Sources",
        "United States. Declaration of Independence"
      ],
      "title": "The Declaration of Independence of the United States of America"
    }
  ],
  "count": 1,
  "next": 0,
  "previous": 0
}

```

### Local testing of API

If you want to test this API locally then you would need to do the following:
1. Obviously download the repo and install dependencies mentioned in requirements.txt.
2. Setup a PostgresSQL or MySQL database and import data from respective data dumps:
PostgresSQL data : https://drive.google.com/file/d/1NJVtOs4Zxk3Go1S9oeurI3pBNH1YWN85/view
MySQL data       : https://drive.google.com/file/d/1Q3QZcy3fmltgLIwLsldPx_KYBOTNuAGA/view
3. Create the database view (script available in sql directory) in your database.
4. Update .env file with database connection details and that should get you moving.
