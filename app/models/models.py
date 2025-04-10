from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    favorites = db.relationship('Favorite', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    preferences = db.relationship('Preference', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_favorite(self, article_id):
        return Favorite.query.filter_by(user_id=self.id, article_id=article_id).first() is not None


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Source(db.Model):
    __tablename__ = 'sources'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    url = db.Column(db.String(256), unique=True)
    description = db.Column(db.Text)
    logo_url = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    articles = db.relationship('Article', backref='source', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Source {self.name}>'


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    content = db.Column(db.Text)
    url = db.Column(db.String(512), unique=True)
    published_at = db.Column(db.DateTime, index=True)
    image_url = db.Column(db.String(512))
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Article {self.title}>'


class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Favorite {self.user_id}:{self.article_id}>'


class Preference(db.Model):
    __tablename__ = 'preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Preference {self.user_id}:{self.source_id}>'
