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


class Trip(db.Model):
    __tablename__ = 'trip'
    id = db.Column(db.Integer, primary_key=True)
    tripId = db.Column(db.Integer)
    tripType = db.Column(db.String(10))
    tripDate = db.Column(db.String(10))
    nameIndex = db.Column(db.String(50))
    tripNo = db.Column(db.String(20))
    tripDepname = db.Column(db.String(20))
    tripArrname = db.Column(db.String(20))
    tripDepcou = db.Column(db.String(20))
    tripArrcou = db.Column(db.String(20))
    tripDeppro = db.Column(db.String(20))
    tripDepcity = db.Column(db.String(20))
    tripArrpro = db.Column(db.String(20))
    tripArrcity = db.Column(db.String(20))
    tripDepcode = db.Column(db.String(10))
    tripArrcode = db.Column(db.String(10))
    tripDeptime = db.Column(db.String(20))
    tripArrtime = db.Column(db.String(20))
    carriage = db.Column(db.String(20))
    seatNo = db.Column(db.String(20))
    tripMemo = db.Column(db.String(100))
    link = db.Column(db.String(100))
    publisher = db.Column(db.String(20))
    publishtime = db.Column(db.String(20))
    verified = db.Column(db.Integer)
    codeList = db.Column(db.String(50))
    createtime = db.Column(db.String(20))
    updatetime = db.Column(db.String(20))


