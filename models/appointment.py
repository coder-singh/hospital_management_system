from db import db


class AppointmentModel(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    appointment_date = db.Column(db.String(10))

    doctor = db.relationship('DoctorModel')
    patient = db.relationship('PatientModel')

    def __init__(self, patient_id, doctor_id, appointment_date):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date

    def json(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'appointment_date': self.appointment_date
        }

    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    @classmethod
    def filter_by_patient_id(cls, patient_id):
        return cls.query.filter_by(patient_id=patient_id)

    @classmethod
    def filter_by_doctor_id(cls, doctor_id):
        return cls.query.filter_by(doctor_id=doctor_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

