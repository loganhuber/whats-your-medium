from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
from routes import register_routes
from config import Config
from models import db, User, ContentBlock, Category, Image, FAQ
from admin_views import AdminModelView, SecureAdminIndexView, ContentBlocksModelView, CategoriesModelView, ImagesModelView, FAQModelView
from pathlib import Path
from flask_migrate import Migrate
from services.storage_service import StorageService
# from werkzeug.security import generate_password_hash

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
db.init_app(app)
storage_service = StorageService(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

admin = Admin(app, index_view=SecureAdminIndexView())

admin.add_view(AdminModelView(User, db, name='Users'))
admin.add_view(ContentBlocksModelView(ContentBlock, db, name='Content'))
admin.add_view(CategoriesModelView(Category, db, name='Categories'))
admin.add_view(
    ImagesModelView(
        Image,
        db,
        storage_service=storage_service,
    ))
admin.add_view(FAQModelView(FAQ, db, name='FAQ'))

register_routes(app)    

if __name__ in '__main__':
    app.run(debug=True)

