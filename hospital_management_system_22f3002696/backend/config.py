class Config:
    SECRET_KEY = "your-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///hospital.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "jwt-secret-key"
    JWT_TOKEN_LOCATION = ["headers"]                  # ← ADD THIS
    JWT_HEADER_NAME = "Authorization"                 # ← ADD THIS
    JWT_HEADER_TYPE = "Bearer"                        # ← ADD THIS
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"