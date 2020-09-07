# Full Stack Capstone Project

This project is the final capstone project for the [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044)

## Casting Agency

The Casting Agency models a company that is responsible for managing movies and actors.

The task for this project was to create the APIs and the test cases for the APIs to implement the follwoing functionalities:
1) Search for actors/movies
2) Create a new actor/movie. 
3) Delete an existing actor/movie.
4) Update an existing actor/movie. 

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/)

No frontend is developed for this app, you can access the backend endpoints using cURL or [Postman](https://www.postman.com)

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Postgres, Python3 and pip installed.

#### Installing Dependencies

First you need to have your virtual enviroment setup and running using the following commands:
```
$ virtualenv --no-site-packages env
$ source env/bin/activate
```
Then run `$ pip install requirements.txt`. The requirements file includes all the required packages. 

## Running the server

Run the following commands: 
```
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask run
```

The application is run on `http://127.0.0.1:5000/` by default. 

## Testing
In order to run the tests located in `test_app.py`, you will first need to create a test database called casting_agency_test. 
Run the following commands:
```
dropdb casting_agency_test
createdb casting_agency_test
psql casting_agency_test < casting_agency_test.psql
python test_app.py
```

## API Reference

### Getting Started
- Base URL: [https://udacity-capstone-fsnd.herokuapp.com](https://udacity-capstone-fsnd.herokuapp.com)

- Authentication: This app has 3 users. All users have different roles with their corresponding tokens. All tokens are provided in the `test_app.py` file. Details about each user's role are provided below:
  - Casting Assistant:
	  - Can view actors and movies

  - Casting Director:
	  - All permissions of a Casting Assistant and…
	  - Add or delete an actor from the database
	  - Modify actors or movies

  - Executive Producer:
	  - All permissions of a Casting Director and…
	  - Add or delete a movie from the database

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return many error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- The last error handler uses AuthError which is set in the `auth.py` file

### Endpoints

#### GET /actors
```
$ curl -H "Authorization: Bearer <ACCESS_TOKEN>" -X GET https://udacity-capstone-fsnd.herokuapp.com/actors
```
- fetches all actors from the database
- sample response:
```
{
    "actors": [
        {
            "age": 45,
            "gender": "male",
            "id": 1,
            "name": "Leonardo DiCaprio"
        }
    ],
    "success": true
}
```

#### GET /movies
```
$ curl -H "Authorization: Bearer <ACCESS_TOKEN>" -X GET https://udacity-capstone-fsnd.herokuapp.com/movies
```
- fetches all movies from the database
- sample response:
```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Wed, 10 Mar 2010 00:00:00 GMT",
            "title": "Shutter Island"
        }
    ],
    "success": true
}
```
#### POST /actors
```
$ curl -H "Authorization: Bearer <ACCESS_TOKEN>" -X POST -d '{"name":"Leonardo DiCaprio","age":45, "gender":"male"}' https://udacity-capstone-fsnd.herokuapp.com/actors
```
- adds a new actor to the database
- sample response:
```
{
    "actor": 
        {
            "age": 45,
            "gender": "male",
            "id": 1,
            "name": "Leonardo DiCaprio"
        },
    "success": true
}
```
#### POST /movies
```
$ curl -H "Authorization: Bearer <ACCESS_TOKEN>" -X POST -d '{"title":"Shutter Island","release_date":"03-10-2010"}' https://udacity-capstone-fsnd.herokuapp.com/movies
```
- adds a new movie to the database
- sample response:
```
{
    "movie":
        {
            "id": 1,
            "release_date": "Wed, 10 Mar 2010 00:00:00 GMT",
            "title": "Shutter Island"
        }
    ],
    "success": true
}
```
#### PATCH /actors
```
$ curl -H "Authorization: Bearer <ACCESS_TOKEN>" -X PATCH -d '{"name":"Leonardo Di Caprio"}' https://udacity-capstone-fsnd.herokuapp.com/actors/1
```
- modifies an existing actor in the database
- sample response:
```
{
    "actor": 
        {
            "age": 45,
            "gender": "male",
            "id": 1,
            "name": "Leonardo Di Caprio"
        },
    "success": true
}
```
#### PATCH /movies
```
$ curl -H "Authorization: Bearer <ACCESS_TOKEN>" -X PATCH -d '{"title":"shutter island"}' https://udacity-capstone-fsnd.herokuapp.com/movies/1
```
- modifies an existing movie in the database
- sample response:
```
{
    "movie":
        {
            "id": 1,
            "release_date": "Wed, 10 Mar 2010 00:00:00 GMT",
            "title": "shutter island"
        }
    ],
    "success": true
}
```
#### DELETE /actors
```
$ curl -H "Authorization: Bearer <ACCESS_TOKEN>" -X DELETE https://udacity-capstone-fsnd.herokuapp.com/actors/1
```
- deletes an existing actor from the database
- sample response:
```
{
    "deleted": 1,
    "success": true
}
```
#### PATCH /movies
```
$ curl -H "Authorization: Bearer <ACCESS_TOKEN>" -X DELETE https://udacity-capstone-fsnd.herokuapp.com/movies/1
```
- deletes an existing movie from the database
- sample response:
```
{
    "deleted": 1,
    "success": true
}
```


## Authors
Noha Salama has deveopled all files in this repo.

## Acknowledgements 
The awesome team at Udacity
