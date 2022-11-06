import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r'/*':{'origins':'*'}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = {}
            for c in Category.query.all():
                categories[c.id] = c.type
            return jsonify({
                "success": True, 
                'categories':categories
            })
        except Exception as e:
            print(e)
            abort(500)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page',default = 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        
        try:
            questions =[q.format() for q in Question.query.all()]
            categories = {}
            for c in Category.query.all():
                categories[c.id] = c.type
            return jsonify({
                "success": True, 
                'questions': questions[start:end],
                'totalQuestions': len(questions),
                'categories':categories,
                'currentCategory': "Sports"
            })
        except Exception as e:
            print(e)
            abort(500)
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):
        try:
            question = Question.query.filter_by(id = question_id).one()
            question.delete()
            return jsonify({
                'success': True
            })
        except Exception as e:
            print(e)
            abort(500)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        try:
            data = request.json
            question = Question(data.get('question'), data.get('answer'), data.get('category'), data.get('difficulty'))
            question.insert()
            return jsonify({
                'success': True
            })
        except Exception as e:
            print(e)
            abort(500)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search():
        try:
            searchTerm = request.json.get('searchTerm')
            questions = Question.search_by_question(searchTerm)
            return jsonify({
                "success": True, 
                'questions': questions,
                'totalQuestions': len(questions),
                'currentCategory':'Sport'
            })
        except Exception as e:
            print(e)
            abort(500)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_question_by_category(category_id):
        try:
            category = Category.query.filter_by(id = category_id).one_or_none()
        except:
            abort(500)
        if category is None:
            abort(404)
        try:
            questions = [q.format() for q in Question.query.filter_by(category_id = category_id)]
            return jsonify({
                "success": True, 
                'questions': questions,
                'totalQuestions': len(questions),
                'currentCategory': "Sports"
            })
        except Exception as e:
            print(e)
            abort(500)
        
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        try:
            pre_question_ids = request.json.get('previous_questions')
            quiz_category = request.json.get('quiz_category').get('id')
            category_count = len(Question.query.all()) if quiz_category == 0 else len(Question.query.filter_by(category_id = quiz_category).all())
            if len(pre_question_ids) < category_count:
                new_question = Question.get_new_question(pre_question_ids, quiz_category)
                return jsonify({
                    "question": new_question
                })
            else:
                return jsonify({
                    "forceEnd": True
                })
        except Exception as e:
            print(e)
            abort(500)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Resource not found."
            }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Request cannot be processed."
            }), 422
        
    @app.errorhandler(409)
    def server_error(error):
        return jsonify({
            "success": False, 
            "error": 409,
            "message": "Resource already exists."
            }), 409
        
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "Something went wrong!"
            }), 500

    return app

