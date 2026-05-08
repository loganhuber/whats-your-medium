from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from config import Config

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    pw_hash = db.Column(db.String(255), nullable=False)


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category_name = db.relationship("Category", backref='images')
    storage_key = db.Column(db.String(255), nullable=False)

    @property
    def url(self):
        return f"https://{Config.DO_SPACES_REGION}.digitaloceanspaces.com/{Config.DO_SPACES_BUCKET}/{self.storage_key}"
        

# category for images
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), nullable=False)

class ContentBlock(db.Model):
    __tablename__ = 'content_blocks'

    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

class FAQ(db.Model):
    __tablename__ = 'faqs'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=False)

    