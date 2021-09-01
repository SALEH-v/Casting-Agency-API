# Casting Agency API - Capstone project

This is a capstone project for Udacity Full-stack development. The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. Me as an Executive Producer within the company and should be creating a system to simplify and streamline the process. So the objective here is to bulid a backend API for this casting agency.

The app is hosted on heroku [Casting Agency API](https://my-casting-agency-api.herokuapp.com/)



## Getting Started

### Installing Dependencies

#### Python 3.9

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Working within a virtual environment is recommended.

#### PIP Dependencies

```bash
pip install -r requirements.txt
```

This will install all of the required packages in the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Database Setup
You need to create a postgres database and change the DATABASE_URL in the setup.sh.
After that you need to run : ``flask db upgrade`` to run the Migrations and create all the tables in the database.


## Auth0 Setup

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
- `get:actors` `get:movies` `post:actors` `post:movies` `patch:actors` `patch:movies` `delete:actors` `delete:movies`
6. Create new roles for:
    - *Casting Assistant* can 
    `get:actors` `get:movies`
    - *Casting Director* can 
    `get:actors` `get:movies` `post:actors` `delete:actors` `patch:actors` `patch:movies`
    - *Executive Producer* can 
    `get:actors` `get:movies` `post:actors` `post:movies` `patch:actors` `patch:movies` `delete:actors` `delete:movies`

    Then you should add the AUTH0_DOMAIN to the setup.sh


## Run the setup.sh file

```bash
source setup.sh
```
OR

```bash
bash setup.sh
```


## Running the server

To run the server:

```bash
export FLASK_APP=app.py
export FLASK_DEBUG=true
flask run
```
OR on windows:

```bash
set FLASK_APP=app.py
set FLASK_DEBUG=true
flask run
```

## Testing
To run the tests, after you change the DATABASE_URL_TEST in the setup.sh:
```
python test_app.py
```

## API Reference

### Getting Started

* Base URL: this application is hosted on heroku: .The backend app is hosted at the default `http://127.0.0.1:5000/`
* Authentication: This version of the application require authentication or API keys using Auth0 (The setup is givin in Auth0 setup section)

### Error Handling

Errors are returned as JSON in the following format:<br>

    {
        "success": False,
        "error": 400,
        "message": "Bad request"
    }

The error codes currently returned are:
* 401 - Unauthorized 
* 400 – bad request
* 404 – resource not found
* 422 – unprocessable
* 500 – internal server error
* 405 - method not allowed


### Endpoints

The endpoints are:
- GET/actors
- GET/movies
- POST/actors
- POST/movies
- PATCH/actors/{id}
- PATCH/movies/{id}
- DELETE/actors/{id}
- DELETE/movies/{id}


#### GET/movies

- General: 
  - Returns all the movies.

- Sample:  `curl http://127.0.0.1:5000/actors`

```json
{
    "movies": [
        {
            "id": 1,
            "release_date": "Thu, 07 Aug 2008 00:00:00 GMT",
            "title": "The dark night"
        },
        {
            "id": 2,
            "release_date": "Thu, 14 Mar 1974 00:00:00 GMT",
            "title": "The godfather"
        },
        {
            "id": 3,
            "release_date": "Mon, 22 Apr 2019 00:00:00 GMT",
            "title": "Avengers: Endgame"
        }
    ],
    "success": true
}
```

#### GET/actors
- General:
  - Returns all actors

- Sample: `curl http://127.0.0.1:5000/actors`<br>

```json
{
    "actors": [
        {
            "age": 47,
            "gender": "male",
            "id": 1,
            "name": "Christian Bale"
        },
        {
            "age": 81,
            "gender": "male",
            "id": 2,
            "name": "Al Pacino"
        },
        {
            "age": 56,
            "gender": "male",
            "id": 3,
            "name": "Robert Downey Jr"
        }
    ],
    "success": true
}
```
#### POST/movies


- General:
  - create a new movies.

- Sample: `curl http://127.0.0.1:5000/movies -X POST -H "Authorization: Bearer <your access token>" -H "Content-Type: application/json" -data '{ "title": "test movie", "release_date": "2021-01-01" }'`<br>

```json
{
    "new_movies": [
        {
            "id": 8,
            "release_date": "Fri, 01 Jan 2021 00:00:00 GMT",
            "title": "test movie"
        }
    ],
    "success": true
}
```

#### POST/actors


* General:
  * Creates a new actor

* Sample: `curl http://127.0.0.1:5000/actors -X POST -H "Authorization: Bearer <your access token>" -H "Content-Type: application/json" -data '{ "name": "test actor", "age": "40", "gender": "male" }'`<br>


```json
  {
    "new_actors": [
        {
            "age": 40,
            "gender": "male",
            "id": 6,
            "name": "test actor"
        }
    ],
    "success": true
}
```




#### PATCH/movies

* General:
  * Update a movie by the ID.

* Sample: `curl http://127.0.0.1:5000/movies/8 -X PATCH -H "Authorization: Bearer <your access token>" -H "Content-Type: application/json" -data '{ "title": "test update movie", "release_date": "2010-10-10" }'`<br>

```json
	 {
    "success": true,
    "updated_movie": [
        {
            "id": 8,
            "release_date": "Sun, 10 Oct 2010 00:00:00 GMT",
            "title": "test update movie"
        }
    ]
}
```

#### PATCH/actors

* General:
  * Update an actor by the ID.

* Sample: `curl http://127.0.0.1:5000/actors/6 -X PATCH -H "Authorization: Bearer <your access token>" -H "Content-Type: application/json" -data '{ "name": "test update actor", "age": "33", "gender": "female" }'`<br>

```json
{
    "success": true,
    "updated_actor": [
        {
            "age": 33,
            "gender": "female",
            "id": 6,
            "name": "test update actor"
        }
    ]
}


```


#### DELETE/movies

* General:
  * Delete a movie by the ID.

* Sample: `curl http://127.0.0.1:5000/movies/8 -X DELETE -H "Authorization: Bearer <your access token>" -H "Content-Type: application/json"`<br>

```json
{
    "deleted_movie": [
        {
            "id": 8,
            "release_date": "Sun, 10 Oct 2010 00:00:00 GMT",
            "title": "test update movie"
        }
    ],
    "success": true
}
```

#### DELETE/actors

* General:
  * Delete an actor by the ID.

* Sample: `curl http://127.0.0.1:5000/actors/6 -X DELETE -H "Authorization: Bearer <your access token>" -H "Content-Type: application/json"`<br>

```json
{
    "deleted_actor": [
        {
            "age": 33,
            "gender": "female",
            "id": 6,
            "name": "test update actor"
        }
    ],
    "success": true
}
```

## Authors

- Udacity provided the specifications
- Saleh worked on everything with this the API.

## Motivation

- My motivation for this project is to complete my nano-degree projects, and this will help me alot to improve my coding skills.
