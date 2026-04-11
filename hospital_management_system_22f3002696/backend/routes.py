from flask import jsonify, request
from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from app import app
from extensions import db, redis_client
from model import User, Department, Doctor, Patient, Appointment, Treatment
import json

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = User.query.get(int(get_jwt_identity()))
        if not user or user.role != "admin":
            return jsonify({"error": "Admin access only"}), 403
        return fn(*args, **kwargs)
    return wrapper

def doctor_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = User.query.get(int(get_jwt_identity()))
        if not user or user.role != "doctor":
            return jsonify({"error": "Doctor access only"}), 403
        return fn(*args, **kwargs)
    return wrapper

def patient_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = User.query.get(int(get_jwt_identity()))
        if not user or user.role != "patient":
            return jsonify({"error": "Patient access only"}), 403
        return fn(*args, **kwargs)
    return wrapper

@app.route("/")
def index():
    return jsonify({"message": "Hospital Management System Running"})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password required"}), 400
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401
    if user.is_blacklisted:
        return jsonify({"error": "Account is blacklisted"}), 403
    if not user.is_active:
        return jsonify({"error": "Account is inactive"}), 403
    token = create_access_token(identity=str(user.id))
    return jsonify({"token": token, "role": user.role, "name": user.name})

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 409
    user = User(
        name=data["name"],
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        role="patient",
        is_active=True,
        is_blacklisted=False
    )
    db.session.add(user)
    db.session.flush()
    patient = Patient(
        user_id=user.id,
        age=data.get("age"),
        gender=data.get("gender"),
        phone=data.get("phone"),
        address=data.get("address")
    )
    db.session.add(patient)
    db.session.commit()
    redis_client.delete("admin_dashboard")
    return jsonify({"message": "Registered successfully"})

@app.route("/api/admin/dashboard")
@admin_required
def admin_dashboard():
    cached = redis_client.get("admin_dashboard")
    if cached:
        return jsonify(json.loads(cached))
    data = {
        "total_doctors": Doctor.query.count(),
        "total_patients": Patient.query.count(),
        "total_appointments": Appointment.query.count()
    }
    redis_client.setex("admin_dashboard", 300, json.dumps(data))
    return jsonify(data)

@app.route("/api/admin/add-doctor", methods=["POST"])
@admin_required
def add_doctor():
    data = request.json
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 409
    dept_name = data.get("department_name", "General")
    dept = Department.query.filter_by(name=dept_name).first()
    if not dept:
        dept = Department(name=dept_name, description=f"{dept_name} Department")
        db.session.add(dept)
        db.session.flush()
    user = User(
        name=data["name"],
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        role="doctor",
        is_active=True,
        is_blacklisted=False
    )
    db.session.add(user)
    db.session.flush()
    doctor = Doctor(
        user_id=user.id,
        department_id=dept.id,
        specialization=data.get("specialization"),
        is_active=True
    )
    db.session.add(doctor)
    db.session.commit()
    redis_client.delete("admin_dashboard")
    return jsonify({"message": f"Doctor added to {dept_name}"})

@app.route("/api/admin/update-doctor/<int:id>", methods=["PUT"])
@admin_required
def update_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    data = request.json
    if data.get("department_name"):
        dept_name = data["department_name"]
        dept = Department.query.filter_by(name=dept_name).first()
        if not dept:
            dept = Department(name=dept_name, description=f"{dept_name} Department")
            db.session.add(dept)
            db.session.flush()
        doctor.department_id = dept.id
    doctor.specialization = data.get("specialization", doctor.specialization)
    doctor.is_active = data.get("is_active", doctor.is_active)
    db.session.commit()
    redis_client.delete("admin_dashboard")
    return jsonify({"message": "Doctor updated"})

@app.route("/api/admin/remove-doctor/<int:id>", methods=["DELETE"])
@admin_required
def remove_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    db.session.delete(doctor)
    db.session.commit()
    redis_client.delete("admin_dashboard")
    return jsonify({"message": "Doctor removed"})

@app.route("/api/admin/update-patient/<int:patient_id>", methods=["PUT"])
@admin_required
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    data = request.json
    patient.age = data.get("age", patient.age)
    patient.phone = data.get("phone", patient.phone)
    patient.address = data.get("address", patient.address)
    db.session.commit()
    return jsonify({"message": "Patient updated"})

@app.route("/api/admin/search")
@admin_required
def admin_search():
    name = request.args.get("name")
    specialization = request.args.get("specialization")
    if name:
        users = User.query.filter(User.name.ilike(f"%{name}%")).all()
        return jsonify([{"id": u.id, "name": u.name, "role": u.role, "email": u.email} for u in users])
    if specialization:
        doctors = Doctor.query.filter(Doctor.specialization.ilike(f"%{specialization}%")).all()
        return jsonify([{"id": d.id, "specialization": d.specialization} for d in doctors])
    return jsonify({"error": "Provide name or specialization param"}), 400

@app.route("/api/admin/search-patient")
@admin_required
def admin_search_patient():
    name = request.args.get("name")
    phone = request.args.get("phone")
    user_id = request.args.get("id")
    result = []
    if user_id:
        user = User.query.get(int(user_id))
        if not user:
            return jsonify({"error": "User not found"}), 404
        patient = Patient.query.filter_by(user_id=user.id).first()
        result = [{"id": user.id, "name": user.name, "email": user.email,
                   "phone": patient.phone if patient else "N/A",
                   "address": patient.address if patient else "N/A",
                   "age": patient.age if patient else "N/A"}]
    elif phone:
        patients = Patient.query.filter(Patient.phone.ilike(f"%{phone}%")).all()
        for p in patients:
            u = User.query.get(p.user_id)
            result.append({"id": u.id, "name": u.name, "email": u.email,
                           "phone": p.phone, "address": p.address, "age": p.age})
    elif name:
        users = User.query.filter(User.name.ilike(f"%{name}%"), User.role == "patient").all()
        for u in users:
            p = Patient.query.filter_by(user_id=u.id).first()
            result.append({"id": u.id, "name": u.name, "email": u.email,
                           "phone": p.phone if p else "N/A",
                           "address": p.address if p else "N/A",
                           "age": p.age if p else "N/A"})
    else:
        return jsonify({"error": "Provide name, phone, or id"}), 400
    return jsonify(result)

@app.route("/api/admin/blacklist/<int:user_id>", methods=["PUT"])
@admin_required
def blacklist_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_blacklisted = True
    db.session.commit()
    return jsonify({"message": f"{user.name} has been blacklisted", "is_blacklisted": True})

@app.route("/api/admin/whitelist/<int:user_id>", methods=["PUT"])
@admin_required
def whitelist_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_blacklisted = False
    db.session.commit()
    return jsonify({"message": f"{user.name} has been whitelisted", "is_blacklisted": False})

@app.route("/api/admin/doctors")
@admin_required
def get_all_doctors():
    doctors = Doctor.query.all()
    result = []
    for d in doctors:
        user = User.query.get(d.user_id)
        dept = Department.query.get(d.department_id)
        result.append({
            "id": d.user_id,
            "doctor_id": d.id,
            "name": user.name,
            "email": user.email,
            "specialization": d.specialization,
            "department": dept.name if dept else "N/A",
            "is_active": d.is_active,
            "is_blacklisted": user.is_blacklisted
        })
    return jsonify(result)

@app.route("/api/admin/patients")
@admin_required
def get_all_patients():
    patients = Patient.query.all()
    result = []
    for p in patients:
        user = User.query.get(p.user_id)
        result.append({
            "id": user.id,
            "patient_id": p.id,
            "name": user.name,
            "email": user.email,
            "phone": p.phone,
            "age": p.age,
            "address": p.address,
            "is_blacklisted": user.is_blacklisted
        })
    return jsonify(result)

@app.route("/api/admin/appointments")
@admin_required
def admin_appointments():
    appointments = Appointment.query.all()
    result = []
    for a in appointments:
        patient = Patient.query.get(a.patient_id)
        doctor = Doctor.query.get(a.doctor_id)
        patient_user = User.query.get(patient.user_id) if patient else None
        doctor_user = User.query.get(doctor.user_id) if doctor else None
        result.append({
            "id": a.id,
            "patient_name": patient_user.name if patient_user else "N/A",
            "doctor_name": doctor_user.name if doctor_user else "N/A",
            "date": a.date,
            "time": a.time,
            "status": a.status
        })
    return jsonify(result)

@app.route("/api/doctor/dashboard")
@doctor_required
def doctor_dashboard():
    user_id = int(get_jwt_identity())
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    return jsonify({
        "total_appointments": len(appointments),
        "pending": sum(1 for a in appointments if a.status == "pending"),
        "completed": sum(1 for a in appointments if a.status == "completed")
    })

@app.route("/api/doctor/appointments")
@doctor_required
def doctor_appointments():
    user_id = int(get_jwt_identity())
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    result = []
    for a in appointments:
        patient = Patient.query.get(a.patient_id)
        patient_user = User.query.get(patient.user_id) if patient else None
        result.append({
            "id": a.id,
            "patient_name": patient_user.name if patient_user else "N/A",
            "date": a.date,
            "time": a.time,
            "status": a.status
        })
    return jsonify(result)

@app.route("/api/doctor/patients")
@doctor_required
def doctor_patients():
    user_id = int(get_jwt_identity())
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    patient_ids = list(set(a.patient_id for a in appointments))
    result = []
    for pid in patient_ids:
        p = Patient.query.get(pid)
        u = User.query.get(p.user_id)
        result.append({"patient_id": p.id, "name": u.name, "age": p.age, "phone": p.phone})
    return jsonify(result)

@app.route("/api/doctor/patient-history/<int:patient_id>")
@doctor_required
def doctor_patient_history(patient_id):
    appointments = Appointment.query.filter_by(patient_id=patient_id).all()
    result = []
    for a in appointments:
        treatment = Treatment.query.filter_by(appointment_id=a.id).first()
        result.append({
            "appointment_id": a.id,
            "date": a.date,
            "time": a.time,
            "status": a.status,
            "diagnosis": treatment.diagnosis if treatment else None,
            "prescription": treatment.prescription if treatment else None,
            "notes": treatment.notes if treatment else None,
            "next_visit_date": treatment.next_visit_date if treatment else None
        })
    return jsonify(result)

@app.route("/api/doctor/appointment/<int:id>/complete", methods=["PUT"])
@doctor_required
def complete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    appointment.status = "completed"
    db.session.commit()
    redis_client.delete("admin_dashboard")
    return jsonify({"message": "Appointment marked completed"})

@app.route("/api/doctor/appointment/<int:id>/cancel", methods=["PUT"])
@doctor_required
def doctor_cancel_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    appointment.status = "cancelled"
    db.session.commit()
    redis_client.delete("admin_dashboard")
    return jsonify({"message": "Appointment cancelled"})

@app.route("/api/doctor/treatment/<int:appointment_id>", methods=["POST"])
@doctor_required
def add_treatment(appointment_id):
    data = request.json
    treatment = Treatment.query.filter_by(appointment_id=appointment_id).first()
    if treatment:
        treatment.diagnosis = data.get("diagnosis", treatment.diagnosis)
        treatment.prescription = data.get("prescription", treatment.prescription)
        treatment.notes = data.get("notes", treatment.notes)
        treatment.next_visit_date = data.get("next_visit_date", treatment.next_visit_date)
    else:
        treatment = Treatment(
            appointment_id=appointment_id,
            diagnosis=data.get("diagnosis"),
            prescription=data.get("prescription"),
            notes=data.get("notes"),
            next_visit_date=data.get("next_visit_date")
        )
        db.session.add(treatment)
    db.session.commit()
    return jsonify({"message": "Treatment saved"})

@app.route("/api/doctor/set-availability", methods=["PUT"])
@doctor_required
def set_availability():
    user_id = int(get_jwt_identity())
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    data = request.json
    doctor.availability_json = json.dumps(data.get("availability"))
    db.session.commit()
    return jsonify({"message": "Availability updated"})

@app.route("/api/patient/profile", methods=["PUT"])
@patient_required
def update_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    patient = Patient.query.filter_by(user_id=user_id).first()
    data = request.json
    user.name = data.get("name", user.name)
    patient.age = data.get("age", patient.age)
    patient.phone = data.get("phone", patient.phone)
    patient.address = data.get("address", patient.address)
    patient.gender = data.get("gender", patient.gender)
    db.session.commit()
    return jsonify({"message": "Profile updated"})

@app.route("/api/patient/departments")
@patient_required
def get_departments():
    departments = Department.query.all()
    return jsonify([{"id": d.id, "name": d.name, "description": d.description} for d in departments])

@app.route("/api/patient/doctors")
@patient_required
def get_doctors():
    dept_id = request.args.get("department_id")
    query = Doctor.query.filter_by(is_active=True)
    if dept_id:
        query = query.filter_by(department_id=dept_id)
    doctors = query.all()
    result = []
    for d in doctors:
        user = User.query.get(d.user_id)
        if user.is_blacklisted:
            continue
        dept = Department.query.get(d.department_id)
        result.append({
            "id": d.id,
            "name": user.name,
            "specialization": d.specialization,
            "department": dept.name if dept else "N/A"
        })
    return jsonify(result)

@app.route("/api/patient/search-doctors")
@patient_required
def patient_search_doctors():
    specialization = request.args.get("specialization", "")
    name = request.args.get("name", "")
    if specialization:
        doctors = Doctor.query.filter(
            Doctor.specialization.ilike(f"%{specialization}%"),
            Doctor.is_active == True
        ).all()
    elif name:
        users = User.query.filter(User.name.ilike(f"%{name}%"), User.role == "doctor").all()
        doctors = []
        for u in users:
            d = Doctor.query.filter_by(user_id=u.id, is_active=True).first()
            if d:
                doctors.append(d)
    else:
        return jsonify({"error": "Provide specialization or name"}), 400
    result = []
    for d in doctors:
        user = User.query.get(d.user_id)
        if user.is_blacklisted:
            continue
        dept = Department.query.get(d.department_id)
        result.append({
            "id": d.id,
            "name": user.name,
            "specialization": d.specialization,
            "department": dept.name if dept else "N/A"
        })
    return jsonify(result)

@app.route("/api/patient/availability/<int:doctor_id>")
@patient_required
def get_availability(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    availability = json.loads(doctor.availability_json) if doctor.availability_json else []
    return jsonify({"availability": availability})

@app.route("/api/patient/doctor-profile/<int:doctor_id>")
@patient_required
def doctor_profile(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    user = User.query.get(doctor.user_id)
    if user.is_blacklisted:
        return jsonify({"error": "This doctor is not available"}), 403
    dept = Department.query.get(doctor.department_id)
    availability = json.loads(doctor.availability_json) if doctor.availability_json else []
    return jsonify({
        "id": doctor.id,
        "name": user.name,
        "email": user.email,
        "specialization": doctor.specialization,
        "department": dept.name if dept else "N/A",
        "availability": availability
    })

@app.route("/api/patient/book", methods=["POST"])
@patient_required
def book_appointment():
    data = request.json
    user_id = int(get_jwt_identity())
    doctor = Doctor.query.get(data["doctor_id"])
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404
    doctor_user = User.query.get(doctor.user_id)
    if doctor_user.is_blacklisted:
        return jsonify({"error": "This doctor is not available for booking"}), 403
    existing = Appointment.query.filter_by(
        doctor_id=data["doctor_id"],
        date=data["date"],
        time=data["time"]
    ).first()
    if existing:
        return jsonify({"error": "This slot is already booked"}), 409
    patient = Patient.query.filter_by(user_id=user_id).first()
    appointment = Appointment(
        patient_id=patient.id,
        doctor_id=data["doctor_id"],
        date=data["date"],
        time=data["time"],
        status="pending"
    )
    db.session.add(appointment)
    db.session.commit()
    redis_client.delete("admin_dashboard")
    return jsonify({"message": "Appointment booked successfully"})

@app.route("/api/patient/cancel/<int:id>", methods=["PUT"])
@patient_required
def cancel_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    appointment.status = "cancelled"
    db.session.commit()
    redis_client.delete("admin_dashboard")
    return jsonify({"message": "Appointment cancelled"})

@app.route("/api/patient/history")
@patient_required
def patient_history():
    user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(user_id=user_id).first()
    appointments = Appointment.query.filter_by(patient_id=patient.id).all()
    result = []
    for a in appointments:
        doctor = Doctor.query.get(a.doctor_id)
        doctor_user = User.query.get(doctor.user_id) if doctor else None
        treatment = Treatment.query.filter_by(appointment_id=a.id).first()
        result.append({
            "id": a.id,
            "doctor_name": doctor_user.name if doctor_user else "N/A",
            "date": a.date,
            "time": a.time,
            "status": a.status,
            "diagnosis": treatment.diagnosis if treatment else None,
            "prescription": treatment.prescription if treatment else None,
            "next_visit_date": treatment.next_visit_date if treatment else None
        })
    return jsonify(result)

@app.route("/api/patient/export-csv", methods=["POST"])
@patient_required
def trigger_export():
    from tasks.task import export_patient_csv
    user_id = int(get_jwt_identity())
    export_patient_csv.delay(user_id)
    return jsonify({"message": "Export started! You will receive an email shortly."})
