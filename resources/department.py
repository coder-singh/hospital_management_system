from flask import request

from flask_restful import reqparse, Resource
from models.department import DepartmentModel


class DepartmentListAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, location='json', required=True, help='name is required')

    def get(self):
        if 'name' in request.args:
            departments = DepartmentModel.filter_by_name(request.args.get('name'))
        else:
            departments = DepartmentModel.fetch_all()
        departments = [patient.json() for patient in departments]
        return departments, 200

    def post(self):
        data = DepartmentListAPI.parser.parse_args()
        department = DepartmentModel(
            name=data['name']
        )
        try:
            department.save_to_db()
        except:
            return {"message": "An error occurred inserting the patient."}, 500
        return department.json(), 201


class DepartmentAPI(Resource):

    def get(self, id_):
        department = DepartmentModel.find_by_id(id_)
        if not department:
            return {
                "msg": "Department not found"
            }, 404
        return department.json(), 200
