import unittest
from extensions import db, create_app


class DepartmentTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app(env='Test')
        with self.app.app_context():
            db.create_all()
        self.tester = self.app.test_client()

    def test_post_201(self):
        response = self.tester.post('/v1/departments', json={
            'name': 'ENT',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            '{"id": 1, "name": "ENT"}\n',
            response.text
        )

    def test_get_404(self):
        response = self.tester.get('/v1/department/10')
        self.assertEqual(404, response.status_code)
        self.assertEqual('{"msg": "Department not found"}\n', response.text)

    def test_get_200(self):
        self.tester.post('/v1/departments', json={
            'name': 'ENT',
        })
        response = self.tester.get('/v1/department/1')
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            '{"id": 1, "name": "ENT"}\n',
            response.text
        )

    def test_get_search_200(self):
        # Creating 2 test records
        self.tester.post('/v1/departments', json={
            'name': 'ENT'
        })
        self.tester.post('/v1/departments', json={
            'name': 'Ortho'
        })
        # Searching records with name Satyendra
        response = self.tester.get('/v1/departments?name=orthO')
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            '[{"id": 2, "name": "Ortho"}]\n',
            response.text
        )

        # Searching records with name Satyendra
        response = self.tester.get('/v1/departments?name=Neuro')
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            '[]\n',
            response.text
        )

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

