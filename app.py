from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
from routes import register_routes
from config import Config
from models import db, User, ContentBlock
from werkzeug.security import generate_password_hash
from admin_views import AdminModelView, SecureAdminIndexView, ContentBlocksModelView

app = Flask(__name__, instance_relative_config=True)

app.config.from_object(Config)
db.init_app(app)

admin = Admin(app, index_view=SecureAdminIndexView())

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

admin.add_view(AdminModelView(User, db))
admin.add_view(ContentBlocksModelView(ContentBlock, db.session))

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
