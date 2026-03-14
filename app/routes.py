from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from app import db
from app.models import (
    Service, Projet, Equipe, Temoignage, Statistique,
    Configuration, Article, ZoneCouverture
)

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    services = Service.query.order_by(Service.ordre).all()
    projets = Projet.query.limit(6).all()
    equipe = Equipe.query.all()
    temoignages = Temoignage.query.all()
    stats = Statistique.query.all()
    return render_template('index.html',
                           services=services,
                           projets=projets,
                           equipe=equipe,
                           temoignages=temoignages,
                           stats=stats)

@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['password'] == 'admin123':  # change ce mot de passe
            session['admin_logged_in'] = True
            return redirect(url_for('admin.index'))
        else:
            flash('Mot de passe incorrect')
    return render_template('admin_login.html')

@bp.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('main.index'))

@bp.route('/blog')
def blog_list():
    articles = Article.query.filter_by(actif=True).order_by(Article.date.desc()).all()
    return render_template('blog_list.html', articles=articles)

@bp.route('/blog/<int:id>')
def blog_detail(id):
    article = Article.query.get_or_404(id)
    return render_template('blog_detail.html', article=article)

@bp.route('/couverture')
def couverture():
    zones = ZoneCouverture.query.all()
    return render_template('couverture.html', zones=zones)

@bp.route('/services')
def services_list():
    services = Service.query.order_by(Service.ordre).all()
    return render_template('services.html', services=services)

@bp.route('/projets')
def projets_list():
    projets = Projet.query.all()
    return render_template('projets.html', projets=projets)

@bp.route('/projet/<int:id>')
def project_detail(id):
    projet = Projet.query.get_or_404(id)
    return render_template('project_detail.html', projet=projet)

@bp.route('/equipe')
def equipe_list():
    equipe = Equipe.query.all()
    return render_template('equipe.html', equipe=equipe)

@bp.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')