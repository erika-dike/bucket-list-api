[![Build Status](https://travis-ci.org/andela-cdike/bucket-list-api.svg?branch=develop)](https://travis-ci.org/andela-cdike/bucket-list-api)
[![Coverage Status](https://coveralls.io/repos/github/andela-cdike/bucket-list-api/badge.svg?branch=develop)](https://coveralls.io/github/andela-cdike/bucket-list-api?branch=develop)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/andela-cdike/bucket-list-api/badges/quality-score.png?b=develop)](https://scrutinizer-ci.com/g/andela-cdike/bucket-list-api/?branch=develop)

## Bucket List API

### Table of Content
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [API Resource Endpoints](#api-resource-endpoints)
4. [Usage](#usage)
5. [Other Features](#other-features)
6. [Running Tests](#running-tests)
7. [Project Demo](#project-demo)

### <a name="introduction"></a>Introduction
BucketListAPI is a REST API that allows users to create, view, update and delete records stored in a database on the applications backend. It only permits SSL connections and token authentication to improve secure access.

### <a name="installation"></a>Installation
1) Clone the repo `$ git clone https://github.com/andela-cdike/bucket-list-api.git`.
2) Navigate to the project folder downloaded.
3) Create and activate a virtual environment.
4) Install dependencies  `$ pip install -r requirements.txt`
5) Run the migration script to setup database:
    * Create migrations by running `$ python manage.py db migrate`.
    * Apply migrations with `$ python manage.py db upgrade`.
6) Run the server using `$ python manage.py runserver`.

### <a name="api-resource-endpoints"></a>API Resource Endpoints
| EndPoint                             | Functionality                 | Public Access       |
| ------------------------------------ | ----------------------------- | ------ |
| POST /auth/register                  | Register a user               | TRUE   |
| POST /auth/login                     | Logs a user in                | TRUE   |
| POST /bucketlists/                   | Create a new bucket list      | FALSE  |
| GET /bucketlists/                    | List all created bucket lists | FALSE  |
| GET /bucketlists/id                  | Get single bucket list        | FALSE  |
| PUT /bucketlists/id                  | Update this bucket list       | FALSE  |
| DELETE /bucketlists/id               | Delete this bucket list       | FALSE  |
| POST /bucketlists/id                 | Create a new item bucket list | FALSE  |
| PUT /bucketlists/id/items/item_id    | Update a bucket list item     | FALSE  |
| DELETE /bucketlists/id/items/item_id | Delete an item in bucket list | FALSE  |

### <a name="usage"></a>Usage
Its important to state here again that only SSL (i.e. https) is supported by this API. Sending a valid request to resources specified above would give registered and logged in users access to the API and to whatever they have stored in the database.

1) To create a new user on your local system. Fire the server, then run:

```cmd 
curl -i -X POST -H "Content-Type: application/json" -d '{"username":"rikky", "password":"python"}' http://127.0.0.1:5000/api/v1.0/auth/register
```

2. Login is similar:
    
```cmd
curl -i -X POST -H "Content-Type: application/json" -d '{"username":"rikky", "password":"python"}' http://127.0.0.1:5000/api/v1.0/auth/register
```

3. A token would be returned to the user which should be attached to subsequent calls to permitted access to other resources. 

4. An example usage with token:

```cmd
curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ2NDYwNjE1Ny:unused -i -X POST -H "Content-Type: application/json" -d '{"name":"Bucketlist1"}' http://127.0.0.1:5000/api/v1.0/bucketlists/
```

5. An example of a GET request:

```cmd
curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ2NDYwNjE1NywiaWF0IjoxNDY0NjAyNTU3fQ.eyJpZCI6N30.JnBM3zCVg_0ulFMa9tw_KmrG0LUPQRlD68lWnclVS1A:unused -i -X GET -H "Content-Type: application/json" http://127.0.0.1:5000/api/v1.0/bucketlists/
```

6. An example of a PUT request:

```cmd
curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ2NDYxMDA0OCwiaWF0IjoxNDY0NjA2NDQ4fQ.eyJpZCI6N30.o8frSCQjHBDOoVlVp_eM1nvje66ulqzJk_NwPGZtJws:unused -i -X PUT -H "Content-Type: application/json" -d '{"name":"Bucketlist17"}' http://127.0.0.1:5000/api/v1.0/bucketlists/2
```

7. An example of DELETE request:

```cmd
curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ2NDYxMDA0OCwiaWF0IjoxNDY0NjA2NDQ4fQ.eyJpZCI6N30.o8frSCQjHBDOoVlVp_eM1nvje66ulqzJk_NwPGZtJws:unused -i -X DELETE -H "Content-Type: application/json" http://127.0.0.1:5000/api/v1.0/bucketlists/3
```

### <a name="other-features"></a>Other Features
A GET request to /bucketlists/ returns a paginated result. The API allows you to vary the number of items returned per page by adding a limit query string to the URL like so: 
```cmd
curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ2NDg2NDI3MiwiaWF0IjoxNDY0ODYwNjcyfQ.eyJpZCI6N30.cLQf4kuGljIOvZQguJGEuVWU9rNlfyxwOwZvO8LI6Fw:unused -i -X GET -H "Content-Type: application/json" http://127.0.0.1:5000/api/v1.0/bucketlists\?limit\=20
```

Another useful feauture is a 'q' query string that allows you to search database for a specified string.
```cmd
curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ2NDg2NDI3MiwiaWF0IjoxNDY0ODYwNjcyfQ.eyJpZCI6N30.cLQf4kuGljIOvZQguJGEuVWU9rNlfyxwOwZvO8LI6Fw:unused -i -X GET -H "Content-Type: application/json" http://127.0.0.1:5000/api/v1.0/bucketlists\?q\=bucketlist1
```
### <a name="running-tests"></a>Running Tests
1) Navigate to the project directory.
2) Run ```nosetests --with-coverage``` to run test and check coverage

### <a name="project-demo"></a>Project Demo
Click [here](https://github.com/andela-cdike) to view the project demo