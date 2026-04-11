from flask import Flask
from config import Config
from extensions import db, jwt
from werkzeug.security import generate_password_hash
from flask_cors import CORS 

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)
CORS(app)  

with app.app_context():
    from model import User, Department, Doctor, Patient, Appointment, Treatment

# Create  tables  
    db.create_all()
    print(" Database created")

    #  create admin
    existing_admin = User.query.filter_by(email="admin@gmail.com").first()
    if not existing_admin:
        admin = User(
            name="Admin",
            email="admin@gmail.com",
            role="admin",
            password_hash=generate_password_hash("admin123"),
            is_active=True,
            is_blacklisted=False
        )
        db.session.add(admin)
        db.session.commit()
        print(" Admin created")
    else:
        print("Adminalready exists")

    from routes import *

if __name__ == "__main__":
    app.run(debug=True)