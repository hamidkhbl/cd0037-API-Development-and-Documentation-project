import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test POST Category
    def test_post_category(self):
        category = Category(type='test')
        payload = category.format()
        res = self.client().post('/categories',  json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test GET categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    # Test GET a category
    def test_get_category_404(self):
        res = self.client().get('categories/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    # Test DELETE categories (Method not allowed)
    def test_delete_categories(self):
        res = self.client().delete('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    # Test POST Questions
    def test_post_questions(self):
        question = Question(
            question='test',
            answer='test answer',
            category=1, difficulty=1)
        payload = question.format()
        res = self.client().post('/questions',  json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test POST Questions with empty answer
    def test_post_questions_empty_answer(self):
        question = Question(
            question='test',
            answer=None,
            category=1, difficulty=1)
        payload = question.format()
        res = self.client().post('/questions',  json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)

    # Test POST Questions with string difficulty
    def test_post_questions_string_difficulty(self):
        question = Question(
            question='test',
            answer=None,
            category=1, difficulty='one')
        payload = question.format()
        res = self.client().post('/questions',  json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)

    # Test GET questionss
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))

    # Test GET questions of a categories
    def test_get_questions_of_categories(self):
        category = Category.query.first()
        res = self.client().get('/categories/'+str(category.id)+'/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test GET questions of a categories that does not exists
    def test_get_questions_of_categories_404(self):
        category = 0
        res = self.client().get('/categories/'+str(category)+'/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # Test Delete a question
    def test_delete_question(self):
        question = Question.query.first()
        res = self.client().delete('/questions/'+str(question.id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test Delete a question wrong id
    def test_delete_question_wrong_id(self):
        res = self.client().delete('/questions/0')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)

    # Test search a question
    def test_search_question_random_string(self):
        payload = {
            "searchTerm": "ham"
        }
        res = self.client().post('/questions/search',  json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test search a question existing
    def test_search_question_existing_question(self):
        question = Question.query.first()
        payload = {
            "searchTerm": question.question
        }
        res = self.client().post('/questions/search',  json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))

    # Test search a question with int
    def test_search_question_random_string(self):
        payload = {
            "searchTerm": 1223
        }
        res = self.client().post('/questions/search', json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)

    # Test quizzes
    def test_quizze(self):
        category = Category.query.first().format()
        payload = {
            'previous_questions': [],
            'quiz_category': category
        }
        res = self.client().post('/quizzes',  json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))

    # Test quizzes
    def test_quizze_when_category_does_not_exists(self):
        category = {
            'type': 'someNoneExistingQuery'
        }
        payload = {
            'previous_questions': [],
            'quiz_category': category
        }
        res = self.client().post('/quizzes',  json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['forceEnd'], True)

    """
    TODO
    Write at least one test for each test
    for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
