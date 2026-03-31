from flask import Flask, session, redirect, url_for, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView, expose # <--- CORRIGÉ ICI
from flask_admin.contrib.sqla import ModelView
import os
from werkzeug.utils import secure_filename
from flask_admin.form import FileUploadField
from flask_babel import Babel
from datetime import datetime

# Initialisation
db = SQLAlchemy()
migrate = Migrate()
babel = Babel()

def get_locale():
    return 'fr'

BASE_IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'static', 'images')

# --- SÉCURITÉ ET STYLE DE BASE ---
class AdminModelView(ModelView):
    # Injection du CSS personnalisé pour le look "Luxe"
    extra_css = ['/static/css/admin_custom.css']
    
    def is_accessible(self):
        return session.get('admin_logged_in', False) or current_app.debug

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.admin_login'))

# Accueil de l'admin avec support pour les statistiques
class MyAdminIndexView(AdminIndexView):
    extra_css = ['/static/css/admin_custom.css']

    def is_accessible(self):
        return session.get('admin_logged_in', False) or current_app.debug

    @expose('/')
    def index(self):
        from app.models import Service, Projet, Equipe, Article
        # On prépare les données pour ton futur Dashboard
        stats = {
            'services': Service.query.count(),
            'projets': Projet.query.count(),
            'equipe': Equipe.query.count(),
            'articles': Article.query.count()
        }
        return self.render('admin/index.html', stats=stats)

# --- VUES SPÉCIFIQUES ---

class ProjetAdminView(AdminModelView):
    form_extra_fields = {
        'image_upload': FileUploadField('Image du Projet', base_path=BASE_IMAGE_PATH, allowed_extensions=['jpg', 'png', 'webp'])
    }
    def on_model_change(self, form, model, is_created):
        if form.image_upload.data:
            filename = secure_filename(form.image_upload.data.filename)
            model.image = filename
        super().on_model_change(form, model, is_created)

class EquipeAdminView(AdminModelView):
    form_extra_fields = {
        'photo_upload': FileUploadField('Photo de profil', base_path=BASE_IMAGE_PATH, allowed_extensions=['jpg', 'png'])
    }
    def on_model_change(self, form, model, is_created):
        if form.photo_upload.data:
            filename = secure_filename(form.photo_upload.data.filename)
            model.photo = filename
        super().on_model_change(form, model, is_created)

class ArticleAdminView(AdminModelView):
    form_extra_fields = {
        'image_upload': FileUploadField('Image de Couverture', base_path=BASE_IMAGE_PATH)
    }
    def on_model_change(self, form, model, is_created):
        if form.image_upload.data:
            model.image = secure_filename(form.image_upload.data.filename)
        super().on_model_change(form, model, is_created)

# --- FACTORY ---

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app, locale_selector=get_locale)

    from app import routes
    app.register_blueprint(routes.bp)

    from app.models import Configuration
    @app.context_processor
    def inject_global_data():
        return dict(config=Configuration.get_singleton(), now=datetime.now())

    # Initialisation Admin avec le thème Bootstrap 4 et l'accueil personnalisé
    admin = Admin(app, name='Telecom Admin', index_view=MyAdminIndexView())
    
    from app.models import Service, Projet, Equipe, Temoignage, Statistique, Article, ZoneCouverture

    # Ajout des vues avec ICÔNES FontAwesome pour un rendu propre
    admin.add_view(AdminModelView(Service, db.session, name="Services", menu_icon_type='fa', menu_icon_value='fa-concierge-bell'))
    admin.add_view(ProjetAdminView(Projet, db.session, name="Projets", menu_icon_type='fa', menu_icon_value='fa-tasks'))
    admin.add_view(EquipeAdminView(Equipe, db.session, name="Équipe", menu_icon_type='fa', menu_icon_value='fa-users'))
    admin.add_view(AdminModelView(Temoignage, db.session, name="Témoignages", menu_icon_type='fa', menu_icon_value='fa-star'))
    admin.add_view(AdminModelView(Statistique, db.session, name="Données Stats", menu_icon_type='fa', menu_icon_value='fa-chart-bar'))
    admin.add_view(AdminModelView(Configuration, db.session, name="Paramètres", menu_icon_type='fa', menu_icon_value='fa-tools'))
    admin.add_view(ArticleAdminView(Article, db.session, name="Blog/Actus", menu_icon_type='fa', menu_icon_value='fa-feather-alt'))
    admin.add_view(AdminModelView(ZoneCouverture, db.session, name="Couverture", menu_icon_type='fa', menu_icon_value='fa-broadcast-tower'))

    if not os.path.exists(BASE_IMAGE_PATH):
        os.makedirs(BASE_IMAGE_PATH)

    return app