from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField
from flask import current_app
from flask_login import current_user
from flask_admin import AdminIndexView, expose
from flask import redirect, url_for
from werkzeug.security import generate_password_hash
from werkzeug.datastructures import FileStorage
from wtforms import PasswordField, FileField
from pathlib import Path
from markupsafe import Markup
from flask_admin.contrib.sqla.fields import QuerySelectField


class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
    
    @expose('/')
    def index(self):
        return self.render(
            'admin/index.html',
            user=current_user.username
        )

class SecureModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


class AdminModelView(SecureModelView):
    form_excluded_columns = ('pwd')
    column_exclude_list = ['pwd']

    form_extra_fields = {
        'password' : PasswordField("Password")
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.pwd = generate_password_hash(form.password.data)


class CategoriesModelView(SecureModelView):
    column_list = ['id', 'category_name']
    form_excluded_columns = ['images']

    column_labels = {
        'id' : 'ID',
        'category_name' : 'Category'
    }

class ContentBlocksModelView(SecureModelView):
    form_columns = ('key', 'value')
    column_list = ['key', 'value', 'updated_at']

    column_labels = {
        "key" : "Key",
        "value" : "Content",
        'updated_at' : "Updated at:"
    }

class ImagesModelView(SecureModelView):
    extra_js = ['static/javascript/compressImg.js']
        