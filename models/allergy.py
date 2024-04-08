from db import db


class AllergyModel(db.Model):
    __tablename__ = 'allergies'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    allergy = db.Column(db.String(50))

    patient = db.relationship('PatientModel')

    def __init__(self, patient_id, allergy):
        self.patient_id = patient_id
        self.allergy = allergy

    def json(self):
        return self.allergy

    @classmethod
    def filter_by_patient_id(cls, patient_id):
        return cls.query.filter_by(patient_id=patient_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

