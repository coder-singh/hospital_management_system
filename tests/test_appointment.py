import unittest
from extensions import db, create_app


class AppointmentTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app(env='Test')
        with self.app.app_context():
            db.create_all()
        self.tester = self.app.test_client()

    def test_post_201(self):
        self.tester.post('/v1/patients', json={
            'name': 'Satyendra',
            'age': 25,
            'gender': 'm',
            'contact': '8888888889'
        })
        self.tester.post('/v1/doctors', json={
            'name': 'Mehek',
            'specialization': 'surgery',
            'contact': '8888888889'
        })
        response = self.tester.post('/v1/appointments', json={
            'patient_id': 1,
            'doctor_id': 1,
            'appointment_date': '10-04-2023'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            '{"id": 1, "patient_id": 1, "doctor_id": 1, "appointment_date": "10-04-2023"}\n',
            response.text
        )

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

