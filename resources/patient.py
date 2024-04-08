from flask import request

from flask_restful import reqparse, Resource

from models.doctor import DoctorModel
from models.patient import PatientModel


class PatientListAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, location='json', required=True, help='name is required')
    parser.add_argument('age', type=int, location='json', required=True, help='age is required')
    parser.add_argument('gender', type=str, location='json', required=True, help='gender is required')
    parser.add_argument('contact', type=str, location='json', required=True, help='contact is required')

    def get(self):
        if 'name' in request.args:
            patients = PatientModel.filter_by_name(request.args.get('name'))
        else:
            patients = PatientModel.fetch_all()
        patients = [patient.json() for patient in patients]
        return patients, 200

    def post(self):
        data = PatientListAPI.parser.parse_args()
        patient = PatientModel(
            name=data['name'],
            age=data['age'],
            contact=data['contact'],
            gender=data['gender']
        )
        try:
            patient.save_to_db()
        except:
            return {"message": "An error occurred inserting the patient."}, 500
        return patient.json(), 201


class PatientAPI(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, location='json', required=True, help='name is required')
    parser.add_argument('age', type=int, location='json', required=True, help='age is required')
    parser.add_argument('gender', type=str, location='json', required=True, help='gender is required')
    parser.add_argument('contact', type=str, location='json', required=True, help='contact is required')

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    def get(self, id_):
        patient = PatientModel.find_by_id(id_)
        self.logger.info(f"Fetching patient by id {id_}")
        if not patient:
            return {
                "msg": "Patient not found"
            }, 404
        return patient.json(), 200

    def put(self, id_):
        patient = PatientModel.find_by_id(id_)
        if not patient:
            return {
                "msg": "Patient not found"
            }, 404
        data = PatientAPI.parser.parse_args()
        patient.name = data['name']
        patient.age = data['age']
        patient.contact = data['contact']
        patient.gender = data['gender']
        try:
            patient.save_to_db()
        except:
            return {"message": "An error occurred updating the patient."}, 500
        return patient.json(), 201

    def delete(self, id_):
        patient = PatientModel.find_by_id(id_)
        if not patient:
            return {
                "msg": "Patient not found"
            }, 404
        try:
            patient.delete_from_db()
        except:
            return {"message": "An error occurred deleting the patient."}, 500
        return patient.json(), 204


class PatientAppointmentListAPI(Resource):
    def get(self, id_):
        patient = PatientModel.find_by_id(id_)
        if not patient:
            return {
                "msg": "Patient not found"
            }, 404
        appointments = [appointment.json() for appointment in patient.appointments]
        return appointments, 200


class PatientDoctorAssignmentAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('doctor_id', type=int, location='json', required=True, help='doctor_id is required')

    def post(self, id_):
        patient = PatientModel.find_by_id(id_)
        if not patient:
            return {
                "msg": "Patient not found"
            }, 404
        data = PatientDoctorAssignmentAPI.parser.parse_args()
        doctor = DoctorModel.find_by_id(data['doctor_id'])
        if not doctor:
            return {
                "msg": "Doctor not found"
            }, 404
        patient.doctor_id = data['doctor_id']
        try:
            patient.save_to_db()
        except:
            return {"message": "An error occurred while assigning doctor."}, 500
        return patient.json(), 204

