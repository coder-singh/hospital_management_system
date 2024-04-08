import logging

from flask import Flask
from flask_restful import Api

from resources.appointment import AppointmentListAPI
from resources.medical_history import MedicalHistoryAPI
from resources.patient import PatientAPI, PatientListAPI, PatientAppointmentListAPI, PatientDoctorAssignmentAPI
from resources.department import DepartmentAPI, DepartmentListAPI
from resources.doctor import DoctorListAPI, DoctorAPI, DoctorDepartmentAssignmentAPI
from db import db

from config import mysqlConfig, mysqlConfigTest


def create_app(env):

    app = Flask(__name__)

    app.logger.setLevel(logging.INFO)
    handler = logging.FileHandler('app.log')
    app.logger.addHandler(handler)

    if env == 'Prod':
        app.config['SQLALCHEMY_DATABASE_URI'] = mysqlConfig
    elif env == 'Test':
        app.config['SQLALCHEMY_DATABASE_URI'] = mysqlConfigTest

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    api = Api(app)

    db.init_app(app)

    api.add_resource(PatientAPI, '/v1/patient/<int:id_>', resource_class_kwargs={
        'logger': app.logger
    })
    api.add_resource(PatientListAPI, '/v1/patients')
    api.add_resource(PatientAppointmentListAPI, '/v1/patient/<int:id_>/appointments')
    api.add_resource(PatientDoctorAssignmentAPI, '/v1/patient/<int:id_>/assign-doctor')

    api.add_resource(DepartmentAPI, '/v1/department/<int:id_>')
    api.add_resource(DepartmentListAPI, '/v1/departments')

    api.add_resource(DoctorAPI, '/v1/doctor/<int:id_>')
    api.add_resource(DoctorListAPI, '/v1/doctors')
    api.add_resource(DoctorDepartmentAssignmentAPI, '/v1/doctor/<int:id_>/assign-department')

    api.add_resource(AppointmentListAPI, '/v1/appointments')

    api.add_resource(MedicalHistoryAPI, '/v1/patient/<int:id_>/medical-history')

    return app
