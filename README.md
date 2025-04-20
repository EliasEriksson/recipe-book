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


## Request response for endpoints
### Recipe
#### List
```http request
GET /api/recipes HTTP/1.1
Accept-Language: sv, en-gb;q=0.8, en;q=0.7
```
```http response
HTTP/1.1 200 OK
Content-Type: application/json
[
    {
        "id": "1234",
        "name": "Tårta",
        language_id": "2341"
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
GET /api/recipes/1234/language/1234 HTTP/1.1
Accept-Language: sv, en-gb;q=0.8, en;q=0.7
```
```http response
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "1234",
    "name": "Cake",
    languageId": "1234"
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
    languageId": "2341",
    "languages": [
        {
            "id": "1234",
            "code": "en"
        }
    ]
}
```
#### Update recipe
```http request
PUT /api/recipes/1234/language/1234 HTTP/1.1
Accept-Language: sv, en-gb;q=0.8, en;q=0.7
Content-Type: application/json

{
    "id": "1234,
    "name": "Cake",
    "languageId": "1234"
}
```
```http response
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "1234,
    "name": "Cake",
    "languageId": "1234"
}
```
#### Delete translation
```http request
DELETE /api/recipes/1234/language/1234 HTTP/1.1
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