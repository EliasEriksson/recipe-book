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

Lists recipies in the users most preferred language.
If query parameter ``

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
Link: <?limit=10&offset=0>; rel="first"',
Link: <?limit=10&offset=1>; rel="prev"',
Link: <?limit=10&offset=3>; rel="next"',
Link: <?limit=10&offset=4; rel="last">',

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
    "id": "1234,
    "name": "Cake",
    "languageId": "1234"
}
```

```http response
HTTP/1.1 200 OK
Content-Type: application/json
Link: /api/recipes/1234/languages/2341; rel="alternate"; hreflang="sv"

{
    "id": "1234,
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