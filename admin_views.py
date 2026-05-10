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

    def __init__(self, model, session, storage_service):
        self.storage_service = storage_service

        self.form_extra_fields = {
            'image_file': FileField('Image File')
        }

        super().__init__(model, session)

    def _image_formatter(view, context, model, name):
        if not model.storage_key:
            return ''
        url = f"https://{view.storage_service.region}.digitaloceanspaces.com/{view.storage_service.bucket}/{model.storage_key}"
        return Markup(f'<img src="{url}" style="max-width: 200px;">')
    
    def _category_formatter(view, context, model, name):
        if not model.category_name:
            return ''
        return model.category_name.category_name
    
    def on_model_change(self, form, model, is_created):
        from services.process_img import process_image
        import tempfile
        import shutil

        if is_created:
            model.admin_id = current_user.id

        file_data = form.image_file.data

        if isinstance(file_data, FileStorage) and file_data and file_data.filename:
            # Delete old S3 files if updating
            if model.storage_key:
                try:
                    self.storage_service.delete_image(model.storage_key)
                except Exception as e:
                    print("Error deleting old file from S3:", e)

            # Get category name for S3 path
            category = model.category_name.category_name if model.category_name else 'uncategorized'
            filename = Path(file_data.filename).stem

            # Create temporary directory for processing
            temp_dir = Path(tempfile.mkdtemp())

            try:
                # Process image (saves original and small versions to temp_dir)
                processed_filename = process_image(
                    file_data,
                    filename,
                    temp_dir
                )

                # Upload original file to S3
                original_path = temp_dir / processed_filename
                if original_path.exists():
                    with open(original_path, 'rb') as f:
                        s3_key = self.storage_service.upload_image(f, category, processed_filename)
                    model.storage_key = s3_key

                # Upload small version to S3 if it exists
                small_filename = f"{Path(processed_filename).stem}-small.webp"
                small_path = temp_dir / small_filename

                if small_path.exists():
                    with open(small_path, 'rb') as f:
                        s3_key_small = self.storage_service.upload_image(f, f"{category}-small", small_filename)
                    model.storage_key_small = s3_key_small

            finally:
                # Clean up temporary files
                shutil.rmtree(temp_dir, ignore_errors=True)

        else:
            # prevent FileStorage from being saved
            if not is_created:
                # restore original value from DB
                session = self.session.session if hasattr(self.session, 'session') else self.session
                existing = session.query(type(model)).get(model.id)
                model.storage_key = existing.storage_key
            else:
                model.storage_key = None

    def on_model_delete(self, model):
        if not model.storage_key:
            return

        # Delete original from S3
        try:
            self.storage_service.delete_image(model.storage_key)
        except Exception as e:
            print("Error deleting original from S3:", e)

        # Delete small version from S3
        # Convert: whats-your-medium/uploads/category/{uuid}.webp
        #      to: whats-your-medium/uploads/category-small/{uuid}.webp
        key_parts = model.storage_key.rsplit('/', 1)
        if len(key_parts) == 2:
            dir_path, filename = key_parts
            small_key = f"{dir_path}-small/{filename}"
            try:
                self.storage_service.delete_image(small_key)
            except Exception as e:
                print("Error deleting small version from S3:", e)

    column_formatters = {
        'filename': _image_formatter,
        'category_name': _category_formatter,
    }
    column_labels = {
        'filename': 'Image',
        'category_name': 'Category',
        'description': 'Description',
        'portfolio_img': 'Display in Portfolio',
        'hero_img': 'Display as Hero Image'
    }
    column_list = ['filename', 'description', 'category_name', 'portfolio_img', 'hero_img']
    form_excluded_columns = ['filename', 'storage_key', 'storage_key_small']
