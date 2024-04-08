from db import db


class DoctorModel(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    specialization = db.Column(db.String(20))
    contact = db.Column(db.String(10))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    appointments = db.relationship('AppointmentModel', lazy='dynamic')
    patients = db.relationship('PatientModel', lazy='dynamic')

    department = db.relationship('DepartmentModel')

    def __init__(self, name, specialization, contact):
        self.name = name
        self.specialization = specialization
        self.contact = contact

    def json(self):
        return {
            'id': self.id,
            'department_id': self.department_id,
            'name': self.name,
            'specialization': self.specialization,
            'contact': self.contact
        }

    @classmethod
    def filter_by_availability_and_specialization(cls, specialization, availability_date):
        doctors = cls.query.filter_by(specialization=specialization).all()
        result = []
        for doctor in doctors:
            if doctor.appointments.filter_by(appointment_date=availability_date).count() == 0:
                result.append(doctor)
        return result

    @classmethod
    def find_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
