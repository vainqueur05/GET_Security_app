from flask import Flask, session, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
import os
from werkzeug.utils import secure_filename
from flask_admin.form import FileUploadField

db = SQLAlchemy()
migrate = Migrate()

# Chemin absolu vers le dossier des images (évalué une fois au démarrage)
BASE_IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'static', 'images')

class AdminModelView(ModelView):
    def is_accessible(self):
        return session.get('admin_logged_in', False)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.admin_login'))

class ProjetAdminView(AdminModelView):
    form_extra_fields = {
        'image_upload': FileUploadField(
            'Image du projet',
            base_path=BASE_IMAGE_PATH,
            allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp']
        )
    }
    form_excluded_columns = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not os.path.exists(BASE_IMAGE_PATH):
            os.makedirs(BASE_IMAGE_PATH)

    def on_model_change(self, form, model, is_created):
        if form.image_upload.data:
            filename = secure_filename(form.image_upload.data.filename)
            model.image = filename
        super().on_model_change(form, model, is_created)

class EquipeAdminView(AdminModelView):
    form_extra_fields = {
        'photo_upload': FileUploadField(
            'Photo du membre',
            base_path=BASE_IMAGE_PATH,
            allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp']
        )
    }
    form_excluded_columns = ['photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not os.path.exists(BASE_IMAGE_PATH):
            os.makedirs(BASE_IMAGE_PATH)

    def on_model_change(self, form, model, is_created):
        if form.photo_upload.data:
            filename = secure_filename(form.photo_upload.data.filename)
            model.photo = filename
        super().on_model_change(form, model, is_created)

class ArticleAdminView(AdminModelView):
    form_extra_fields = {
        'image_upload': FileUploadField(
            'Image de l\'article',
            base_path=BASE_IMAGE_PATH,
            allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp']
        )
    }
    form_excluded_columns = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not os.path.exists(BASE_IMAGE_PATH):
            os.makedirs(BASE_IMAGE_PATH)

    def on_model_change(self, form, model, is_created):
        if form.image_upload.data:
            filename = secure_filename(form.image_upload.data.filename)
            model.image = filename
        super().on_model_change(form, model, is_created)

class ZoneCouvertureAdminView(AdminModelView):
    pass

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app import routes
    app.register_blueprint(routes.bp)

    from app.models import Configuration
    @app.context_processor
    def inject_config():
        return dict(config=Configuration.get_singleton())

    admin = Admin(app, name='Telecom Admin', index_view=AdminIndexView())
    from app.models import Service, Projet, Equipe, Temoignage, Statistique, Configuration, Article, ZoneCouverture

    admin.add_view(AdminModelView(Service, db.session))
    admin.add_view(ProjetAdminView(Projet, db.session))
    admin.add_view(EquipeAdminView(Equipe, db.session))
    admin.add_view(AdminModelView(Temoignage, db.session))
    admin.add_view(AdminModelView(Statistique, db.session))
    admin.add_view(AdminModelView(Configuration, db.session))
    admin.add_view(ArticleAdminView(Article, db.session))
    admin.add_view(ZoneCouvertureAdminView(ZoneCouverture, db.session))

    return app