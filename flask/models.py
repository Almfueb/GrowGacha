from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    profile_picture = db.Column(db.String(120), default='default.jpg')
    histories = db.relationship('History', backref='user', lazy=True)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    rarity = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class MDMAccount(db.Model):
    __tablename__ = 'MDMA_accounts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    rarity = db.Column(db.String(100), nullable=False)

class ELITEAccount(db.Model):
    __tablename__ = 'ELITE_accounts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    rarity = db.Column(db.String(100), nullable=False)

class ANCIENTAccount(db.Model):
    __tablename__ = 'ANCIENT_accounts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    rarity = db.Column(db.String(100), nullable=False)