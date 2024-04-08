from flask import request

from flask_restful import reqparse, Resource
from models.department import DepartmentModel
from models.patient import PatientModel


class MedicalHistoryAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('allergies', type=list, location='json', required=True, help='allergies is required')
    parser.add_argument('diagnoses', type=list, location='json', required=True, help='diagnoses is required')
    parser.add_argument('medications', type=list, location='json', required=True, help='medications is required')

    def get(self, id_):
        patient = PatientModel.find_by_id(id_)
        if not patient:
            return {
                "msg": "Patient not found"
            }, 404
        response = {
            "id": patient.id,
            "allergies": [allergy.json() for allergy in patient.allergies.all()],
            "diagnoses": [diagnosis.json() for diagnosis in patient.diagnoses.all()],
            "medications": [medication.json() for medication in patient.medications.all()]
        }
        return response, 200

    def post(self, id_):
        patient = PatientModel.find_by_id(id_)
        if not patient:
            return {
                "msg": "Patient not found"
            }, 404
        data = MedicalHistoryAPI.parser.parse_args()
        try:
            patient.add_medical_history(
                allergies=data['allergies'], diagnoses=data['diagnoses'], medications=data['medications']
            )
        except:
            return {"message": "An error occurred inserting the patient."}, 500
        return '', 201
