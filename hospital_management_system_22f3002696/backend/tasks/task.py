import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from celery import Celery
from celery.schedules import crontab
import csv, io, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import datetime



# STARTING CELERY 

def make_celery():
    celery = Celery(
        "tasks",
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/0"
    )
    celery.conf.beat_schedule = {
        "daily-reminder-8am": {
            "task": "tasks.send_daily_reminders",
           # "schedule": crontab(hour=10, minute=0),
           "schedule": crontab(minute='*/2'),
        },
        "monthly-report-1st": {
            "task": "tasks.send_monthly_report",
           #"schedule": crontab(day_of_month=1, hour=7, minute=0),
           "schedule": crontab(minute='*/2'),
        },
    }
    celery.conf.timezone = "Asia/Kolkata"
    return celery

celery = make_celery()


# EMAIL SENDING CODE

FROM_EMAIL = "riteekkr8@gmail.com"   
PASSWORD   = "aatz wsyq apye zsqk"      

def send_email(to, subject, body, is_html=False, csv_data=None, csv_filename="export.csv"):
    msg = MIMEMultipart()
    msg["From"]    = FROM_EMAIL
    msg["To"]      = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html" if is_html else "plain"))

    if csv_data:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(csv_data.encode())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={csv_filename}")
        msg.attach(part)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(FROM_EMAIL, PASSWORD)
            server.sendmail(FROM_EMAIL, to, msg.as_string())
        print(f"Email sent to {to}")
    except Exception as e:
        print(f"Email failed: {e}")



#  DAILY REMINDER 

@celery.task(name="tasks.send_daily_reminders")
def send_daily_reminders():
    from app import app
    from model import Appointment, Patient, User, Doctor

    with app.app_context():
        today        = datetime.date.today().strftime("%Y-%m-%d")
        appointments = Appointment.query.filter_by(date=today, status="pending").all()
        print(f"Found {len(appointments)} appointments for today {today}")

        for appt in appointments:
            patient = Patient.query.get(appt.patient_id)
            doctor  = Doctor.query.get(appt.doctor_id)
            p_user  = User.query.get(patient.user_id) if patient else None
            d_user  = User.query.get(doctor.user_id)  if doctor  else None

            if p_user and p_user.email:
                send_email(
                    to=p_user.email,
                    subject="Appointment Reminder - Today",
                    body=f"""
                    <p>Dear <strong>{p_user.name}</strong>,</p>
                    <p>You have an appointment scheduled <strong>today ({today})</strong>
                    with Dr. <strong>{d_user.name if d_user else 'N/A'}</strong>
                    at <strong>{appt.time}</strong>.</p>
                    <p>Please visit the hospital on time.</p>
                    """,
                    is_html=True
                )



#  MONTHLY REPORT 

@celery.task(name="tasks.send_monthly_report")
def send_monthly_report():
    from app import app
    from model import Appointment, Doctor, User, Treatment, Patient

    with app.app_context():
        last_month  = (datetime.date.today().replace(day=1) - datetime.timedelta(days=1))
        month_str   = last_month.strftime("%Y-%m")
        month_label = last_month.strftime("%B %Y")

        doctors = Doctor.query.all()
        for doc in doctors:
            d_user = User.query.get(doc.user_id)
            if not d_user or not d_user.email:
                continue

            appointments = Appointment.query.filter(
                Appointment.doctor_id == doc.id,
                Appointment.date.like(f"{month_str}%")
            ).all()

            total     = len(appointments)
            completed = sum(1 for a in appointments if a.status == "completed")
            cancelled = sum(1 for a in appointments if a.status == "cancelled")
            pending   = sum(1 for a in appointments if a.status == "pending")

            rows = ""
            for a in appointments:
                treatment = Treatment.query.filter_by(appointment_id=a.id).first()
                patient   = Patient.query.get(a.patient_id)
                p_user    = User.query.get(patient.user_id) if patient else None
                rows += f"""
                <tr>
                  <td>{a.date}</td>
                  <td>{a.time}</td>
                  <td>{p_user.name if p_user else 'N/A'}</td>
                  <td>{a.status}</td>
                  <td>{treatment.diagnosis    if treatment else '-'}</td>
                  <td>{treatment.prescription if treatment else '-'}</td>
                  <td>{treatment.next_visit_date if treatment else '-'}</td>
                </tr>
                """

            body = f"""
            <p>Dear Dr. <strong>{d_user.name}</strong>,</p>
            <p>Here is your monthly report for <strong>{month_label}</strong>:</p>
            <table border="1" cellpadding="6" cellspacing="0">
              <tr>
                <td>Total</td><td>{total}</td>
                <td>Completed</td><td>{completed}</td>
                <td>Cancelled</td><td>{cancelled}</td>
                <td>Pending</td><td>{pending}</td>
              </tr>
            </table>
            <br>
            <table border="1" cellpadding="6" cellspacing="0">
              <tr>
                <th>Date</th><th>Time</th><th>Patient</th>
                <th>Status</th><th>Diagnosis</th>
                <th>Prescription</th><th>Next Visit</th>
              </tr>
              {rows}
            </table>
            """

            send_email(
                to=d_user.email,
                subject=f"Monthly Report - {month_label}",
                body=body,
                is_html=True
            )
            print(f"Monthly report sent to {d_user.email}")



#  EXPORT PATIENT CSV 

@celery.task(name="tasks.export_patient_csv")
def export_patient_csv(user_id):
    from app import app
    from model import Appointment, Patient, User, Doctor, Treatment

    with app.app_context():
        user    = User.query.get(user_id)
        patient = Patient.query.filter_by(user_id=user_id).first()

        if not user or not patient:
            print(f"User {user_id} not found")
            return

        appointments = Appointment.query.filter_by(patient_id=patient.id).all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Appointment ID", "Doctor", "Date", "Time",
            "Status", "Diagnosis", "Prescription", "Next Visit"
        ])

        for a in appointments:
            doctor    = Doctor.query.get(a.doctor_id)
            d_user    = User.query.get(doctor.user_id) if doctor else None
            treatment = Treatment.query.filter_by(appointment_id=a.id).first()
            writer.writerow([
                a.id,
                d_user.name               if d_user    else "N/A",
                a.date,
                a.time,
                a.status,
                treatment.diagnosis       if treatment else "",
                treatment.prescription    if treatment else "",
                treatment.next_visit_date if treatment else ""
            ])

        send_email(
            to=user.email,
            subject="Your Treatment History - CSV Export",
            body=f"""
            <p>Dear <strong>{user.name}</strong>,</p>
            <p>Please find your treatment history CSV attached.</p>
            """,
            is_html=True,
            csv_data=output.getvalue(),
            csv_filename=f"treatment_history_{user.name}.csv" )
        print(f"CSV exported and sent to {user.email}")