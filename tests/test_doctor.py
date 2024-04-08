import unittest
from extensions import db, create_app


class DoctorTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app(env='Test')
        with self.app.app_context():
            db.create_all()
        self.tester = self.app.test_client()

    def test_post_201(self):
        response = self.tester.post('/v1/doctors', json={
            'name': 'Satyendra',
            'specialization': 'surgery',
            'contact': '8888888889'
        })
        # self.assertEqual(201, response.status_code)
        self.assertEqual(
            '{"id": 1, "department_id": null, "name": "Satyendra", "specialization": "surgery", "contact": "8888888889"}\n',
            response.text
        )

    def test_get_404(self):
        response = self.tester.get('/v1/doctor/10')
        self.assertEqual(404, response.status_code)
        self.assertEqual('{"msg": "Doctor not found"}\n', response.text)

    def test_get_200(self):
        self.tester.post('/v1/doctors', json={
            'name': 'Satyendra',
            'specialization': 'surgery',
            'contact': '8888888889'
        })
        response = self.tester.get('/v1/doctor/1')
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            '{"id": 1, "department_id": null, "name": "Satyendra", "specialization": "surgery", "contact": "8888888889"}\n',
            response.text
        )

    def test_get_search_200(self):
        # Creating 2 test records
        self.tester.post('/v1/doctors', json={
            'name': 'Satyendra',
            'specialization': 'surgery',
            'contact': '8888888889'
        })
        self.tester.post('/v1/doctors', json={
            'name': 'Mehek',
            'specialization': 'pharmacy',
            'contact': '886666689'
        })
        self.tester.post('/v1/patients', json={
            'name': 'Vishal',
            'age': 25,
            'gender': 'm',
            'contact': '8888888889'
        })

        # book for 10-04-2023
        response = self.tester.post('/v1/appointments', json={
            'patient_id': 1,
            'doctor_id': 1,
            'appointment_date': '10-04-2023'
        })

        # Searching records with name Satyendra
        response = self.tester.get('/v1/doctors?specialization=surgery&availability_date=09-04-2023')
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            '[{"id": 1, "department_id": null, "name": "Satyendra", "specialization": "surgery", "contact": "8888888889"}]\n',
            response.text
        )

        # Searching records with name Satyendra
        response = self.tester.get('/v1/doctors?specialization=surgery&availability_date=10-04-2023')
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            '{"msg": "No surgery doctor found for 10-04-2023"}\n',
            response.text
        )

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

