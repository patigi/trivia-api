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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_01_get_categories(self):
        """Test GET for /categories"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['success'])

    def test_02_get_questions_without_pagination(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 19)
        self.assertTrue(data['success'])

    def test_03_get_questions_with_valid_pagination(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 19)
        self.assertTrue(data['success'])

    def test_04_get_questions_with_invalid_pagination(self):
        res = self.client().get('/questions?page=3')

        self.assertEqual(res.status_code, 404)

    def test_05_delete_valid_question(self):
        """ Test for DELETE on /questions/13 """
        old_count = Question.query.count()
        res = self.client().delete('/questions/13')
        new_count = Question.query.count()

        self.assertEqual(res.status_code, 204)
        self.assertNotIn(13, [q.id for q in Question.query.all()])
        self.assertEqual(old_count - 1, new_count)

    def test_06_delete_invalid_question(self):
        res = self.client().delete('/questions/100')

        self.assertEqual(res.status_code, 422)

    def test_07_create_new_valid_question(self):

        old_count = Question.query.count()

        new_question = {
            'question': 'Will this test case pass?',
            'answer': 'Yes! It created this question, so it passes.',
            'category': '5',
            'difficulty': '1'
        }
        res = self.client().post('/questions', json=new_question)

        new_count = Question.query.count()

        data = json.loads(res.data)

        match = new_question
        match['success'] = True

        self.assertTrue(data['question'])
        self.assertTrue(data['answer'])
        self.assertTrue(data['category'])
        self.assertTrue(data['difficulty'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(old_count + 1, new_count)

    def test_08_create_new_invalid_question_wrong_category(self):
        new_question = {
            'question': 'Will this test case pass?',
            'answer': 'Nope! This category does not exist.',
            'category': 10,
            'difficulty': 1
        }
        res = self.client().post('/questions', json=new_question)

        self.assertEqual(res.status_code, 422)

    def test_09_create_new_invalid_question_no_category(self):
        new_question = {
            'question': 'Will this test case pass?',
            'answer': 'Nope! This response has no category.',
            'difficulty': 1
        }
        res = self.client().post('/questions', json=new_question)

        self.assertEqual(res.status_code, 422)

    def test_10_create_new_invalid_question_no_difficulty(self):
        new_question = {
            'question': 'Will this test case pass?',
            'answer': 'Nope! This response has no difficulty.',
            'category': 10,
        }
        res = self.client().post('/questions', json=new_question)

        self.assertEqual(res.status_code, 422)

    def test_11_create_new_invalid_question_wrong_difficulty(self):
        new_question = {
            'question': 'Will this test case pass?',
            'answer': 'Nope! This response has no difficulty.',
            'category': 2,
            'difficulty': 10,
        }
        res = self.client().post('/questions', json=new_question)

        self.assertEqual(res.status_code, 422)

    def test_12_create_new_invalid_question_no_question(self):
        new_question = {
            'answer': 'Nope! This response has no question.',
            'category': 2,
            'difficulty': 2,
        }
        res = self.client().post('/questions', json=new_question)

        self.assertEqual(res.status_code, 422)

    def test_13_create_new_invalid_question_no_answer(self):
        new_question = {
            'question': 'Will this test case pass?',
            'category': 2,
            'difficulty': 2,
        }
        res = self.client().post('/questions', json=new_question)

        self.assertEqual(res.status_code, 422)

    def test_14_search_question_with_results(self):
        search = { 'searchTerm': 'title' }
        res = self.client().post('/search/questions', json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 2)
        self.assertTrue(data['questions'])
        self.assertTrue(data['success'])

    def test_15_search_question_without_results(self):
        search = { 'searchTerm': 'whatever' }
        res = self.client().post('/search/questions', json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(data['questions'], [])
        self.assertTrue(data['success'])

    def test_16_get_questions_by_valid_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(data['total_count']), 3)
        self.assertTrue(data['success'])
        self.assertEqual(int(data['current_category']), 1)
        self.assertTrue(data['questions'])

    def test_17_get_questions_by_invalid_category(self):
        res = self.client().get('/categories/10/questions')

        self.assertEqual(res.status_code, 404)

    def test_18_play_quiz_by_category(self):
        req = {'previous_questions': [20], 'current_category': str(1)}
        res = self.client().post('/quizzes', json=req)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(int(data['question']['id']), 20)

    def test_19_play_quiz(self):
        req = {'previous_questions': [20]}
        res = self.client().post('/quizzes', json=req)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(int(data['question']['id']), 20)

    def test_20_play_quiz_by_category_empty_request(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
