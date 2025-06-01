# Recipe book

## python packages
* uvicorn
* litestar
* SQLAlchemy
* psycopg
* alembic
* msgspec
* click
* Babel

## Setup
### Install non python dependencies
* [postgresql](https://www.postgresql.org/download/)
* `apt install python3.x-dev`\
  `x` is your python 3 minor version
* `apt install build-essential cargo`

### Install python dependencies
1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `python -m pip install -r requirements.txt`

### Configure postgres user
create the recipe-book user and database

```sql
CREATE
DATABASE "recipe-book";
CREATE
DATABASE "recipe-book-test";
-- OBS! Do not use this password for anything other than local development!
CREATE
USER "recipe-book" WITH ENCRYPTED PASSWORD 'recipe-book';
GRANT ALL PRIVILEGES ON DATABASE
"recipe-book" to "recipe-book";
GRANT ALL PRIVILEGES ON DATABASE
"recipe-book-test" to "recipe-book";
-- posgresql 15+
ALTER DATABASE "recipe-book" OWNER TO "recipe-book";
ALTER DATABASE "recipe-book-test" OWNER TO "recipe-book";
```

### Initialize the database
```bash
python main.py database migrate && python main.py database seed
```


## Request response examples for endpoints
### Recipe or any translatable resource
This is examples requests of the recipe resource but any translatable resource will look roughly the same.
For available endpoints and body schemas visit `/api`.
#### List
Lists recipies in the users most preferred language.
* If query parameter `language` is defined it will override the header if present.
* If query parameter `language` is set to the string value `original` the list will recipies with their original language.
  This means that the list may include recipies with mixed languages
* Possible paging is found in the `Link` header. `rel="prev"` and `rel="next"` are only provided if they are relevant.

```http request
GET /api/recipes HTTP/1.1
Accept-Language: sv, en-gb;q=0.8, en;q=0.7
```
```http response
HTTP/1.1 200 OK
Content-Type: application/json
Link: <https://example.com/api/recipes?limit=10&offset=0>; rel="first", <https://example.com/api/recipes?limit=10&offset=3>; rel="next", <https://example.com/api/recipes?limit=10&offset=3>; rel="next", <https://example.com/api/recipes?limit=10&offset=4>; rel="last"'

[
    {
        "id": "1234",
        "name": "Tårta",
        "language_id": "2341"
    }
]
```

#### List available translations
```http request
GET /api/recipes/1234/languages HTTP/1.1
Accept-Language: sv, en-gb;q=0.8, en;q=0.7
```
```http response
HTTP/1.1 200 OK
Content-Type: application/json
Link: <https://example.com/api/recipes/1234/languages?limit=10&offset=0>; rel="first", <https://example.com/api/recipes/1234/languages?limit=10&offset=3>; rel="next", <https://example.com/api/recipes/1234/languages?limit=10&offset=3>; rel="next", <https://example.com/api/recipes/1234/languages?limit=10&offset=4>; rel="last"'

[
    {
        "id": "1234",
        "code", "en"
    },
    {
        "id": "2341",
        "code", "sv"
    }
]
```

#### Fetch one
```http request
GET /api/recipes/1234/languages/1234 HTTP/1.1
Accept-Language: sv, en-gb;q=0.8, en;q=0.7
```
```http response
HTTP/1.1 200 OK
Content-Type: application/json
Link: /api/recipes/1234/languages/2341; rel="alternate"; hreflang="sv"

{
    "id": "1234",
    "name": "Cake",
    "languageId": "1234"
}
```

#### Create
```http request
POST /api/recipes HTTP/1.1
Accept-Language: sv, en-gb;q=0.8, en;q=0.7
Content-Type: application/json

{
    "name": "Cake",
    "languageId": "1234"
}
```
```http response
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "1234",
    "name": "Cake",
    "languageId": "2341"
}
```

#### Update recipe
```http request
PUT /api/recipes/1234/languages/1234 HTTP/1.1
Accept-Language: sv, en-gb;q=0.8, en;q=0.7
Content-Type: application/json

{
    "id": "1234",
    "name": "Cake",
    "languageId": "1234"
}
```
```http response
HTTP/1.1 200 OK
Content-Type: application/json
Link: /api/recipes/1234/languages/2341; rel="alternate"; hreflang="sv"

{
    "id": "1234",
    "name": "Cake",
    "languageId": "1234"
}
```

#### Delete translation
```http request
DELETE /api/recipes/1234/languages/1234 HTTP/1.1
Accept-Language: sv, en-gb;q=0.8, en;q=0.7
```
```http response
HTTP/1.1 204 No Content
```

#### Delete entire recipe and all translations

```http request
DELETE /api/recipes/1234 HTTP/1.1
Accept-Language: sv, en-gb;q=0.8, en;q=0.7
```
```http response
HTTP/1.1 204 No Content
```
