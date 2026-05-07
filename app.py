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
# from werkzeug.security import generate_password_hash

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
db.init_app(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

admin = Admin(app, index_view=SecureAdminIndexView())

admin.add_view(AdminModelView(User, db))
admin.add_view(ContentBlocksModelView(ContentBlock, db))
admin.add_view(CategoriesModelView(Category, db))
admin.add_view(
    ImagesModelView(
        Image,
        db,
        upload_path=Path(app.root_path) / 'static' / 'uploads'
    ))
admin.add_view(FAQModelView(FAQ, db))

register_routes(app)    

if __name__ in '__main__':
    app.run(debug=True)
    # with app.app_context():
    #     # db.create_all()
    #     # print("db created")
    #     pw_hash = generate_password_hash('password')

    #     user = User(
    #         username="logan",
    #         email='cjhuber102@gmail.com',
    #         pw_hash=pw_hash
    #     )
    #     db.session.add(user)
    #     db.session.commit()
    #     print("added user")
