from app import db

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icone = db.Column(db.String(50), nullable=False, default='bi-wifi')
    ordre = db.Column(db.Integer, default=0)

class Projet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200), default='default-project.jpg')
    lien = db.Column(db.String(200))
    date = db.Column(db.String(20))

class Equipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100))
    photo = db.Column(db.String(200), default='default-avatar.jpg')
    description = db.Column(db.Text)

class Temoignage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    note = db.Column(db.Integer)

class Statistique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False)
    valeur = db.Column(db.String(50), nullable=False)
    icone = db.Column(db.String(50), default='bi-bar-chart')

class Configuration(db.Model):
    id = db.Column(db.Integer, primary_key=True, default=1)
    nom_entreprise = db.Column(db.String(100), default='GET Security')
    slogan = db.Column(db.String(200), default='Solutions réseaux fiables')
    hero_image = db.Column(db.String(200), default='hero.jpg')
    apropos = db.Column(db.Text)
    contact_email = db.Column(db.String(100))
    contact_telephone = db.Column(db.String(20))
    localisation = db.Column(db.String(200), default='Lubumbashi, RDC')

    @classmethod
    def get_singleton(cls):
        config = cls.query.get(1)
        if not config:
            config = cls(id=1)
            db.session.add(config)
            db.session.commit()
        return config

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    image = db.Column(db.String(200), default='default-article.jpg')
    resume = db.Column(db.String(300))
    auteur = db.Column(db.String(100), default='Admin')
    actif = db.Column(db.Boolean, default=True)

class ZoneCouverture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)