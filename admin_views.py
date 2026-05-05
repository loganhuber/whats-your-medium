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
from models import Category


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

class FAQModelView(SecureModelView):
    form_columns = ('question', 'answer')
    column_list = ['id', 'question', 'answer']

    column_labels = {
        "id" : "ID",
        "question" : "Question",
        "answer" : "Answer"
    }

class ImagesModelView(SecureModelView):
    extra_js = ['/static/javascript/compressImg.js']

    form_overrides = {
        'category_name': QuerySelectField
    }

    form_args = {
        'category_name': {
            'query_factory': lambda: Category.query.order_by(Category.category_name).all(),
            'allow_blank': True,
            'get_label': lambda c: c.category_name if c else 'None'
        }
    }

    def __init__(self, model, session, upload_path):
        self.upload_path = upload_path

        self.form_extra_fields = {
            'image_file': FileField('Image File')
        }

        super().__init__(model, session)

    def _image_formatter(view, context, model, name):
        if not model.filename:
            return ''
        return Markup(f'<img src="/static/uploads/{model.filename}" style="max-width: 200px;">')
    
    def _category_formatter(view, context, model, name):
        if not model.category_name:
            return ''
        return model.category_name.category_name
    
    def on_model_change(self, form, model, is_created):
        from process_img import process_image

        if is_created:
            model.admin_id = current_user.id

        file_data = form.image_file.data

        if isinstance(file_data, FileStorage) and file_data and file_data.filename:
            if model.filename:
                upload_dir = Path(self.upload_path)

                old_file = upload_dir / model.filename
                small_dir = upload_dir.parent / f"{upload_dir.name}-small"
                old_small = small_dir / f"{Path(model.filename).stem}-small.webp"

                for f in (old_file, old_small):
                    if f.is_file():
                        try:
                            f.unlink()
                        except Exception as e:
                            print("Error deleting old file:", f, e)

            filename = Path(file_data.filename).stem

            processed_filename = process_image(
                file_data,
                filename,
                Path(self.upload_path)
            )

            model.filename = processed_filename

        else:
            # prevent FileStorage from being saved
            # process image already handles saving
            if not is_created:
                # restore original value from DB
                # session may be a scoped_session, so get the actual session if needed
                session = self.session.session if hasattr(self.session, 'session') else self.session
                existing = session.query(type(model)).get(model.id)
                model.filename = existing.filename
            else:
                model.filename = None

    def on_model_delete(self, model):
        if not model.filename:
            return

        upload_dir = Path(self.upload_path)
        # original image
        file_path = upload_dir / model.filename
        # small image directory (e.g. "gallery-small")
        small_dir = upload_dir.parent / f"{upload_dir.name}-small"
        # small image filename
        file_small = small_dir / f"{Path(model.filename).stem}-small.webp"

        for f in (file_path, file_small):
            print("Deleting:", f)

            if f.is_file():
                try:
                    f.unlink()
                except Exception as e:
                    print("Error deleting:", f, e)

    column_formatters = {
        'filename': _image_formatter,
        'category_name': _category_formatter,
    }
    column_labels = {
        'filename': 'Image',
        'category_name': 'Category',
        'description': 'Description'
    }
    column_list = ['filename', 'description', 'category_name']
    form_excluded_columns = ['filename']
