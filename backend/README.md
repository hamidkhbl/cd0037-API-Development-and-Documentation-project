# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation

`GET /categories`

This API returns list of all the categories. Here is an example of the response.
```json
{
    "categories": {
        "1": "Sports",
        "2": "Art"
    },
    "success": true
}
```


`GET /questions`

This API returns list of all the questions.
```json
{
    "categories": {
        "1": "Sports",
        "2": "Art"
    },
    "currentCategory": "Sports",
    "questions": [
        {
            "answer": "test",
            "category": 1,
            "difficulty": 1,
            "id": 1,
            "question": "test"
        },
        {
            "answer": "Art answer",
            "category": 2,
            "difficulty": 1,
            "id": 4,
            "question": "Art question"
        }
    ],
    "success": true,
    "totalQuestions": 2
}
```

`POST /questions`

Using this API you can add a quesion. The payload should look like this.
```json
{
    "question":"a new question",
    "answer": "a new answer",
    "category": 1,
    "difficulty": 5
}
```
The respose includes the id of the added question.
```json
{
    "id": 12,
    "success": true
}
```

`DELETE /questions/<int:question_id>`
This API deletes a question by id. The response looks like this:
```json
{
    "id": 12,
    "success": true
}
```

`POST /questions/search`
This API searches questions and returns a set of results.
The paylod should look like this:
```json
{
    "searchTerm":"test"
}
```
Here is a sample response
```json
{
    "currentCategory": "Sport",
    "questions": [
        {
            "answer": "test",
            "category": 1,
            "difficulty": 1,
            "id": 1,
            "question": "test"
        },
        {
            "answer": "test2",
            "category": 1,
            "difficulty": 1,
            "id": 3,
            "question": "test2"
        }
    ],
    "success": true,
    "totalQuestions": 2
}
```

`GET /categories/<int:category>/questions`
This endpoint returns all the questions of a category
```json
{
    "currentCategory": "Sports",
    "questions": [
        {
            "answer": "test",
            "category": 1,
            "difficulty": 1,
            "id": 1,
            "question": "test"
        },
        {
            "answer": "test2",
            "category": 1,
            "difficulty": 1,
            "id": 3,
            "question": "test2"
        },
        {
            "answer": "first answer",
            "category": 1,
            "difficulty": 1,
            "id": 10,
            "question": "first Hamid"
        },
        {
            "answer": "a new answer",
            "category": 1,
            "difficulty": 5,
            "id": 11,
            "question": "a new question"
        }
    ],
    "success": true,
    "totalQuestions": 4
}
```

`POST /quizzes`
This API returns a question that the id is not included in the previous_questions array. The following payload will return a question from the Art category with id other than 1 or 3.
```json
{
    "previous_questions": [
        1,
        3
    ],
    "quiz_category": {
        "type": "Art",
        "id": 2
    }
}
```
The response for such request will look like this.
```json
{
    "question": {
        "answer": "Art answer",
        "category": 2,
        "difficulty": 1,
        "id": 4,
        "question": "Art question"
    },
    "success": true
}
```
In case all the questions were answered and no question is remaining the response looks like the following to let the UI know that there is no question left.

```json
{
    "forceEnd": true
}
```

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
