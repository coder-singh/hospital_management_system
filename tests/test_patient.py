import unittest
from extensions import db, create_app


class PatientTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app(env='Test')
        with self.app.app_context():
            db.create_all()
        self.tester = self.app.test_client()

    def test_post_201(self):
        response = self.tester.post('/v1/patients', json={
            'name': 'Satyendra',
            'age': 25,
            'gender': 'm',
            'contact': '8888888889'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            '{"id": 1, "doctor_id": null, "name": "Satyendra", "age": 25, "gender": "m", "contact": "8888888889"}\n',
            response.text
        )

    def test_get_404(self):
        response = self.tester.get('/v1/patient/10')
        self.assertEqual(404, response.status_code)
        self.assertEqual('{"msg": "Patient not found"}\n', response.text)

    def test_get_200(self):
        self.tester.post('/v1/patients', json={
            'name': 'Satyendra',
            'age': 25,
            'gender': 'm',
            'contact': '8888888889'
        })
        response = self.tester.get('/v1/patient/1')
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            '{"id": 1, "doctor_id": null, "name": "Satyendra", "age": 25, "gender": "m", "contact": "8888888889"}\n',
            response.text
        )

    def test_put_201(self):
        # Creating a new record for patient
        self.tester.post('/v1/patients', json={
            'name': 'Satyendra',
            'age': 25,
            'gender': 'm',
            'contact': '8888888889'
        })

        # Updating some values using put request
        response = self.tester.put('/v1/patient/1', json={
            'name': 'Satyendra2',
            'age': 26,
            'gender': 'f',
            'contact': '8889990002'
        })
        self.assertEqual(201, response.status_code)

        # Checking if changes were reflected in database
        response = self.tester.get('/v1/patient/1')
        self.assertEqual(
            '{"id": 1, "doctor_id": null, "name": "Satyendra2", "age": 26, "gender": "f", "contact": "8889990002"}\n',
            response.text
        )

    def test_delete_204(self):
        # Creating a new record for patient
        self.tester.post('/v1/patients', json={
            'name': 'Satyendra',
            'age': 25,
            'gender': 'm',
            'contact': '8888888889'
        })

        # deleting this record
        response = self.tester.delete('/v1/patient/1')
        self.assertEqual(204, response.status_code)

        # Checking if the record was deleted
        response = self.tester.get('/v1/patient/1')
        self.assertEqual(
            '{"msg": "Patient not found"}\n',
            response.text
        )

    def test_get_search_200(self):
        # Creating 2 test records
        self.tester.post('/v1/patients', json={
            'name': 'Satyendra',
            'age': 25,
            'gender': 'm',
            'contact': '8888888889'
        })
        self.tester.post('/v1/patients', json={
            'name': 'Mehek',
            'age': 22,
            'gender': 'f',
            'contact': '886666689'
        })
        # Searching records with name Satyendra
        response = self.tester.get('/v1/patients?name=SAtyenDra')
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            '[{"id": 1, "doctor_id": null, "name": "Satyendra", "age": 25, "gender": "m", "contact": "8888888889"}]\n',
            response.text
        )

        response = self.tester.get('/v1/patients')
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            '[{"id": 1, "doctor_id": null, "name": "Satyendra", "age": 25, "gender": "m", "contact": "8888888889"}, '
            '{"id": 2, "doctor_id": null, "name": "Mehek", "age": 22, "gender": "f", "contact": "886666689"}]\n',
            response.text
        )

        # Searching records with name Satyendra
        response = self.tester.get('/v1/patients?name=Nihit')
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            '[]\n',
            response.text
        )

    def test_appointment_200(self):
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
        self.tester.post('/v1/doctors', json={
            'name': 'Vaid',
            'specialization': 'neuro',
            'contact': '8888838889'
        })
        self.tester.post('/v1/appointments', json={
            'patient_id': 1,
            'doctor_id': 1,
            'appointment_date': '10-04-2023'
        })
        self.tester.post('/v1/appointments', json={
            'patient_id': 1,
            'doctor_id': 2,
            'appointment_date': '11-04-2023'
        })
        response = self.tester.get('/v1/patient/1/appointments')
        self.assertEqual(200, response.status_code)
        self.assertEqual('[{"id": 1, "patient_id": 1, "doctor_id": 1, "appointment_date": "10-04-2023"}, '
                         '{"id": 2, "patient_id": 1, "doctor_id": 2, "appointment_date": "11-04-2023"}]\n', response.text)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

