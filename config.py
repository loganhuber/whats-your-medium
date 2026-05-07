import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # UPLOAD_FOLDER = 'static/uploads'

    DO_SPACES_KEY=os.getenv("DO_SPACES_KEY")
    DO_SPACES_SECRET=os.getenv("DO_SPACES_SECRET")
    DO_SPACES_BUCKET=os.getenv("DO_SPACES_BUCKET")
    DO_SPACES_REGION=os.getenv("DO_SPACES_REGION")