from flask_restful import reqparse, Resource

from models.appointment import AppointmentModel


class AppointmentListAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('patient_id', type=int, location='json', required=True, help='patient_id is required')
    parser.add_argument('doctor_id', type=int, location='json', required=True, help='doctor_id is required')
    parser.add_argument('appointment_date', type=str, location='json', required=True, help='date is required')

    def post(self):
        data = AppointmentListAPI.parser.parse_args()
        appointment = AppointmentModel(
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id'],
            appointment_date=data['appointment_date']
        )
        try:
            appointment.save_to_db()
        except:
            return {"message": "An error occurred inserting the appointment."}, 500
        return appointment.json(), 201
