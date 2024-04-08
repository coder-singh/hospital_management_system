from db import db
from models.allergy import AllergyModel
from models.diagnoses import DiagnosesModel
from models.medication import MedicationModel


class PatientModel(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1))
    contact = db.Column(db.String(10))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))

    appointments = db.relationship('AppointmentModel', lazy='dynamic')
    diagnoses = db.relationship('DiagnosesModel', lazy='dynamic')
    allergies = db.relationship('AllergyModel', lazy='dynamic')
    medications = db.relationship('MedicationModel', lazy='dynamic')

    doctor = db.relationship('DoctorModel')

    def __init__(self, name, age, gender, contact):
        self.name = name
        self.age = age
        self.gender = gender
        self.contact = contact

    def json(self):
        return {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'contact': self.contact
        }

    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    @classmethod
    def filter_by_name(cls, name):
        return cls.query.filter_by(name=name)

    @classmethod
    def find_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def add_medical_history(self, allergies, diagnoses, medications):
        for allergy in allergies:
            self.allergies.append(AllergyModel(self.id, allergy))
        for diagnosis in diagnoses:
            self.diagnoses.append(DiagnosesModel(self.id, diagnosis))
        for medication in medications:
            self.medications.append(MedicationModel(self.id, medication))
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
