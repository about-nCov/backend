# coding:utf-8
import json
import time
from . import api
from app import db
from app.models import Inflection, Area
from flask import jsonify, request, Response


@api.route('/inflection/', methods=['POST'])
# @User.token_check(0)
def new_data():
    if request.method == 'POST':
        data = request.get_json()
        feed = Inflection(date=data.get("date"),
                          total=data.get("total"),
                          definite=data.get("definite"),
                          suspected=data.get("suspected"),
                          death=data.get("death"),
                          cured=data.get("cured"),
                          newdefinite=data.get("newdefinite"),
                          newdeath=data.get("newdeath"),
                          newsuspected=data.get("newsuspected"),
                          newcured=data.get("newcured"),
                          )
        db.session.add(feed)
        db.session.commit()
        return jsonify({"msg": "information add successful!"}), 200


@api.route('/inflection/information/', methods=['POST'])
def daily_information():
    if request.method == 'POST':
        date = request.get_json().get("date")
        data = Inflection.query.filter_by(date=date).first()
        if data is None:
            return jsonify({"information": {}}), 201
        definite_increase = "Null"
        if data.newdefinite != 0 and data.definite != data.newdefinite:
            definite_increase = float(data.newdefinite) / float(data.definite-data.newdefinite) * 100
            definite_increase = str(format(definite_increase, '.1f')) + "%"
        suspected_increase = "Null"
        if data.newsuspected != 0 and data.suspected != data.newsuspected:
            suspected_increase = float(data.newsuspected) / float(data.suspected - data.newsuspected) * 100
            suspected_increase = str(format(suspected_increase, '.1f')) + "%"
        death_increase = "Null"
        if data.newdeath != 0 and data.death != data.newdeath:
            death_increase = float(data.newdeath) / float(data.death - data.newdeath) * 100
            death_increase = str(format(death_increase, '.1f')) + "%"
        cured_increase = "Null"
        if data.newcured != 0 and data.cured != data.newcured:
            cured_increase = float(data.newcured) / float(data.cured - data.newcured) * 100
            cured_increase = str(format(cured_increase, '.1f')) + "%"
        information = {"date": data.date,
                       "total": data.total,
                       "definite": data.definite,
                       "suspected": data.suspected,
                       "death": data.death,
                       "cured": data.cured,
                       "newdefinite": data.newdefinite,
                       "definite_increase": definite_increase,
                       "newdeath": data.newdeath,
                       "death_increase": death_increase,
                       "newsuspected": data.newsuspected,
                       "suspected_increase": suspected_increase,
                       "newcured": data.newcured,
                       "cured_increase": cured_increase
                       }
        return jsonify({"information": information}), 200


@api.route('/inflection/area/', methods=['POST'])
def area_information():
    if request.method == 'POST':
        date = request.get_json().get("date")
        country = request.get_json().get("country")
        if country == "":
            country = "中国"
        province = request.get_json().get("province")
        data = Area.query.filter_by(date=date, country=country, province=province).first()
        if data is None:
            return jsonify({"information": {}}), 201
        information = {"date": data.date,
                       "country": data.country,
                       "province": data.province,
                       "definite": data.definite,
                       "suspected": data.suspected,
                       "death": data.death,
                       "cured": data.cured,
                       }
        return jsonify({"information": information}), 200