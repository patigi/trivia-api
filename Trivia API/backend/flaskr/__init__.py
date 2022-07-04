import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    ### CORS functionality
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    ### API Endpoints
    @app.route('/categories', methods=['GET'])
    def get_categories():
      categories = Category.get_all()
      response = {
        'success': True,
        'categories': categories
      }
      return jsonify(response)


    @app.route('/questions')
    def get_questions():
        """
        Creates an endpoint to handle GET requests for questions,
        including pagination (every 10 questions).
        This endpoint returns a list of questions,
        number of total questions, and categories.
        """
        page = request.args.get('page', 1, type=int)
        questions = [q.format()
                    for q in Question.query.order_by('category')\
                    .paginate(page, QUESTIONS_PER_PAGE, True).items]
        response = {
        "success": True,
        "total_questions": Question.query.count(),
        "questions": questions,
        "categories": Category.get_all()
        }
        return jsonify(response)


    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        Creates an endpoint to DELETE a question based on id
        """
        error = False
        try:
          question = Question.query.get(question_id)
          Question.delete(question)
        except:
          error = True
          db.session.rollback()
        finally:
          db.session.close()

        if error:
          abort(422)

        return '', 204


    @app.route('/questions', methods=['POST'])
    def create_question():
        """
        Creates an endpoint to POST a new question,
        which will require the question and answer text,
        category, and difficulty score.
        """
        req = request.get_json()
        error = False

        try:
            if (int(req['category']) not in [c.id for c in Category.query.all()]
              or int(req['difficulty']) not in [1, 2, 3, 4, 5]):
                error = True
            else:
                new_question = Question(
                    question=req['question'],
                    answer=req['answer'],
                    category=req['category'],
                    difficulty=int(req['difficulty'])
                )
                Question.insert(new_question)
        except:
          error = True
          db.session.rollback()
        finally:
          db.session.close()

        if error:
          abort(422)

        response = req
        response['success'] = True
        print(response)
        return jsonify(response)


    @app.route('/search/questions', methods=['POST'])
    def search_questions():
        """
        Create a POST endpoint to get questions based on a search term.
        It should return any questions for whom the search term
        is a substring of the question.
        """
        search_term = request.get_json()['searchTerm']
        question_matches = Question.query.filter(Question.question.ilike(f'%{search_term}%'))
        results = [q.format() for q in question_matches]

        total_count = question_matches.count()

        response = {
        'total_questions': total_count,
        'questions': results,
        'success': True
        }
        print(response)

        return jsonify(response)


    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        """
        Creates a GET endpoint to get questions based on category.
        """
        if int(category_id) not in [c.id for c in Category.query.all()]:
            abort(404)
        questions = [q.format() for q in Question.query.filter_by(category=category_id)]
        response = {
        "success": True,
        "current_category": category_id,
        "total_count": Question.query.filter_by(category=category_id).count(),
        "questions": questions,
        }
        print(response)

        return jsonify(response)


    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        """
        Creates a POST endpoint to get questions to play the quiz.
        This endpoint should take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.
        """
        error = False
        try:
            prev_id_list = request.get_json()['previous_questions']
            category = request.get_json()['quiz_category']
            cat_id = int(category['id'])
            if cat_id != 0:
                if cat_id in [c.id for c in Category.query.all()]:
                    choices = [q.id for q in Question.query.filter_by(category=cat_id).all() if q.id not in prev_id_list]
                    if len(choices) > 0:
                        cur_id = random.choice(choices)
                    else:
                        cur_id = None
                else:
                    error = True
            else:
                choices = [q.id for q in Question.query.all() if q.id not in prev_id_list]
                if len(choices) > 0:
                    cur_id = random.choice(choices)
                else:
                    cur_id = None
        except:
            cur_id = random.choice([q.id for q in Question.query.all()])
        finally:
            if error:
              abort(404)
            if cur_id is None:
                cur_question = None
            else:
                cur_question = Question.query.get(cur_id).format()

        response = {
        'success': True,
        'question': cur_question
        }
        print(response)
        return jsonify(response)

    ### Error handling
    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
          "success": False,
          "message": "Resource not found"
          }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          "success": False,
          "message": "Unprocessable"
          }), 422

    return app
