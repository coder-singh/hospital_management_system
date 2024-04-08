from flask import request

from flask_restful import reqparse, Resource

from models.department import DepartmentModel
from models.doctor import DoctorModel


class DoctorListAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, location='json', required=True, help='name is required')
    parser.add_argument('specialization', type=str, location='json', required=True, help='specialization is required')
    parser.add_argument('contact', type=str, location='json', required=True, help='contact is required')

    def get(self):
        specialization = request.args.get('specialization')
        availability_date = request.args.get('availability_date')
        doctors = DoctorModel.filter_by_availability_and_specialization(specialization=specialization, availability_date=availability_date)
        doctors = [doctor.json() for doctor in doctors]
        if doctors:
            return doctors, 200
        else:
            return {"msg": f"No {specialization} doctor found for {availability_date}"}, 200

    def post(self):
        data = DoctorListAPI.parser.parse_args()
        doctor = DoctorModel(
            name=data['name'],
            specialization=data['specialization'],
            contact=data['contact']
        )
        try:
            doctor.save_to_db()
        except:
            return {"message": "An error occurred inserting the doctor."}, 500
        return doctor.json(), 201


class DoctorAPI(Resource):

    def get(self, id_):
        doctor = DoctorModel.find_by_id(id_)
        if not doctor:
            return {
                "msg": "Doctor not found"
            }, 404
        return doctor.json(), 200


class DoctorDepartmentAssignmentAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('department_id', type=int, location='json', required=True, help='department_id is required')

    def post(self, id_):
        doctor = DoctorModel.find_by_id(id_)
        if not doctor:
            return {
                "msg": "Doctor not found"
            }, 404
        data = DoctorDepartmentAssignmentAPI.parser.parse_args()
        department = DepartmentModel.find_by_id(data['department_id'])
        if not department:
            return {
                "msg": "Department not found"
            }, 404
        doctor.department_id = data['department_id']
        try:
            doctor.save_to_db()
        except:
            return {"message": "An error occurred while assigning department."}, 500
        return doctor.json(), 201
