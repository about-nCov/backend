# coding: utf-8
import json
import time
from . import api
from app import db
from app.models import Trip
from flask import jsonify, request, Response
from sqlalchemy import or_
from . import inflection

en_dict = inflection.en_dict

def date_limiter(date, sp, need_zero):
    time = date.split("/")
    if need_zero == 1:
        month = time[1]
        day = time[2]
    else:
        month = str(int(time[1]))
        day = str(int(time[2]))
    return time[0] + sp + month + sp + day



@api.route('/inflection/trip/', methods=['POST'])
def trip_information():
    if request.method == 'POST':
        date = request.get_json().get("date")
        date = date_limiter(date, '-', 1)
        print(date)
        country = request.get_json().get("country")
        province = request.get_json().get("province")
        city = request.get_json().get('city')
        if country and province and city:
            datas = Trip.query.filter_by(tripDate=date).filter(
                or_(Trip.tripDepcou.like("%" +country+ "%"), 
                    Trip.tripArrcou.like("%" +country+ "%"))
                ).filter(
                or_(Trip.tripDeppro.like("%" +province+ "%"),
                    Trip.tripArrpro.like("%" +province+ "%"))
                ).filter(
                or_(Trip.tripDepcity.like("%" +city+ "%"), 
                    Trip.tripArrcity.like("%" +city+ "%"))
            ).all()
        else:
            datas = Trip.query.filter_by(tripDate=date).all()
        if datas is None:
            return jsonify({"information_list": {}}), 201
        information_list = []
        for data in datas:
            information = {"date": data.tripDate,
                           "type": data.tripType,
                           "tripNo": data.tripNo,
                           "tripDepName": data.tripDepname,
                           "tripArrName": data.tripArrname,
                           "depCountry": data.tripDepcou,
                           "arrCountry": data.tripArrcou,
                           "depProvince": data.tripDeppro,
                           "arrProvince": data.tripArrpro,
                           "depCity": data.tripDepcity,
                           "arrCity": data.tripArrcity,
                           "publishTime": data.publishtime,
                           "link": data.link,
                           "publisher": data.publisher,
                           "carriage": data.carriage,
                           }
            information_list.append(information)
        return jsonify({"information_list": information_list}), 200


@api.route('/inflection/trip/ll/', methods=['POST'])
def trip_information_ll():
    if request.method == 'POST': 
        date = request.get_json().get("date")
        date = date_limiter(date, '-', 1)
        province = request.get_json().get("province")
        country = ""
        datas = Trip.query.filter_by(tripDate=date).filter(
                Trip.tripDeppro != Trip.tripArrpro
                ).filter(Trip.tripDepcity != Trip.tripArrcity
                ).filter(Trip.tripDepcou.like("%" +country+ "%")
                ).filter(Trip.tripArrcou.like("%" +country+ "%")
            ).filter(
            or_(Trip.tripDeppro.like("%" +province+ "%"),
                Trip.tripArrpro.like("%" +province+ "%"),
                Trip.tripDepcity.like("%" +province+ "%"),
                Trip.tripArrcity.like("%" +province+ "%"))
            ).all()
        if datas is None:
            return jsonify({"information_list": []}), 201
        information_list = []
        for data in datas:
            if data.tripDeppro:
                fromName = data.tripDeppro
            else:
                fromName = data.tripDepcity
            if data.tripArrpro:
                toName = data.tripArrpro
            else:
                toName = data.tripArrcity
            if not toName or not fromName:
                continue
            information = {"fromName": fromName,
                           "toName": toName,
                           "coords":[
                                en_dict[fromName],
                                en_dict[toName]
                            ]}
            if information not in information_list:
                information_list.append(information)
        return jsonify({"imformation_list": information_list}), 200


@api.route('/inflection/trip/province/', methods=['POST'])
def trip_information_province():
    if request.method == 'POST': 
        date = request.get_json().get("date")
        date = date_limiter(date, '-', 1)
        datas = Trip.query.filter_by(tripDate=date).filter(
                or_(Trip.tripDeppro==Trip.tripArrpro,
                Trip.tripDepcity==Trip.tripArrcity)
                ).all()
        if datas is None:
            return jsonify({"information_list": []}), 201
        information_list = []
        information_dict = {}
        for data in datas:
            if data.tripDeppro in information_dict:
                information_dict[data.tripDeppro] += 1
            elif data.tripDepcity in information_dict:
                information_dict[data.tripDepcity] += 1
            else:
                if data.tripDeppro:
                    information_dict[data.tripDeppro] = 1 
                else:
                    information_dict[data.tripDepcity] = 1
        for key, value in information_dict.items():
            information = {"province":key,
                           "coords":en_dict[key],
                           "count":value
                    }
            information_list.append(information)
        return jsonify({"imformation_list": information_list}), 200

