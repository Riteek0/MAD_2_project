from extensions import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email  = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20))
    is_active =  db.Column(db.Boolean, default=True)
    is_blacklisted = db.Column(db.Boolean, default=False)
    created_at =  db.Column(db.DateTime, default=datetime.utcnow)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description =  db.Column(db.Text)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id =  db.Column(db.Integer, db.ForeignKey("user.id"))
    department_id =  db.Column(db.Integer, db.ForeignKey("department.id"))
    specialization = db.Column(db.String(100))
    availability_json = db.Column(db.Text)
    is_active =db.Column(db.Boolean, default=True)

class Patient(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    age =  db.Column(db.Integer)
    gender = db.Column(db.String(10))
    phone =db.Column(db.String(15))
    address = db.Column(db.Text)

class Appointment(db.Model):
    __table_args__ =  (db.UniqueConstraint("doctor_id", "date", "time"),)
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"))
    date = db.Column(db.String(20))
    time = db.Column(db.String(10))
    status = db.Column(db.String(20), default="pending")

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.id"))
    diagnosis  = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes =  db.Column(db.Text)
    next_visit_date =  db.Column(db.String(20))