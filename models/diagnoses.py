from db import db


class DiagnosesModel(db.Model):
    __tablename__ = 'diagnoses'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    diagnosis = db.Column(db.String(50))

    patient = db.relationship('PatientModel')

    def __init__(self, patient_id, diagnosis):
        self.patient_id = patient_id
        self.diagnosis = diagnosis

    def json(self):
        return self.diagnosis

    @classmethod
    def filter_by_patient_id(cls, patient_id):
        return cls.query.filter_by(patient_id=patient_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

