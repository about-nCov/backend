# coding :utf-8
from . import db


class Inflection(db.Model):
    __tablename__ = 'inflection'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    total = db.Column(db.Integer)
    definite = db.Column(db.Integer)
    suspected = db.Column(db.Integer)
    death = db.Column(db.Integer)
    cured = db.Column(db.Integer)
    newdefinite = db.Column(db.Integer)
    newdeath = db.Column(db.Integer)
    newsuspected = db.Column(db.Integer)
    newcured = db.Column(db.Integer)


class Area(db.Model):
    __tablename__ = 'area'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    country = db.Column(db.String(20))
    province = db.Column(db.String(20))
    definite = db.Column(db.Integer)
    suspected = db.Column(db.Integer)
    death = db.Column(db.Integer)
    cured = db.Column(db.Integer)

