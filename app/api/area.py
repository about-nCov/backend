# coding:utf-8
import json
import time
from . import api
from app import db
from app.models import Inflection, Area, Trip, Weibo
from flask import jsonify, request, Response
from sqlalchemy import or_


def date_limiter(date, sp, need_zero):
    time = date.split("/")
    if need_zero == 1:
        month = time[1]
        day = time[2]
    else:
        month = str(int(time[1])) 
        day = str(int(time[2])) 
    return time[0] + sp + month + sp + day


@api.route('/inflection/area/', methods=['POST'])
def area_information():
    if request.method == 'POST':
        date = request.get_json().get("date")
        date = date_limiter(date, '/', 0)
        country = request.get_json().get("country")
        if country == "":
            country = "中国"
        province = request.get_json().get("province")
        information_list = []
        if province != "":
            data = Area.query.filter_by(date=date, country=country, province=province).first()
        else:
            all_data = Area.query.filter_by(date=date, country=country).all()
            for data in all_data:
                information = {"date": data.date,
                               "country": data.country,
                               "province": data.province,
                               "definite": data.definite,
                               "suspected": data.suspected,
                               "death": data.death,
                               "cured": data.cured,
                               }
                information_list.append(information)
            return jsonify({"information_list":information_list}),200
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
        information_list.append(information)
        return jsonify({"information": information_list}), 200

