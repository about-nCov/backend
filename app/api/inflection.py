# coding:utf-8
import json
import time
from . import api
from app import db
from app.models import Inflection
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
def data_list():
    if request.method == 'POST':
        date = request.get_json().get("date")
        data = Inflection.query.filter_by(date=date).first()
        information = {"date": data.date,
                       "total": data.total,
                       "definite": data.definite,
                       "suspected": data.suspected,
                       "death": data.death,
                       "cured": data.cured,
                       "newdefinite": data.newdefinite,
                       "newdeath": data.newdeath,
                       "newsuspected": data.newsuspected,
                       "newcured": data.newcured,
                       }
        return jsonify({"information": information}), 200
