# coding:utf-8
import json
import time
from . import api
from app import db
from app.models import Inflection, Area, Trip, Weibo
from flask import jsonify, request, Response
from sqlalchemy import or_


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
            definite_increase = float(data.newdefinite) / float(data.definite - data.newdefinite) * 100
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


@api.route('/inflection/trip/', methods=['POST'])
def trip_information():
    if request.method == 'POST':
        date = request.get_json().get("date")
        country = request.get_json().get("country")
        province = request.get_json().get("province")
        city = request.get_json().get('city')
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
            information = {"fromName": fromName,
                           "toName": toName,
                           "coords":[
                                en_dict[fromName],
                                en_dict[toName]
                            ]}
            if information not in information_list:
                information_list.append(information)
        return jsonify({"imformation_list": information_list}), 200

@api.route('/inflection/weibo/proportion/', methods=['GET'])
def weibo_proportion():
    if request.method == "GET":
        date = request.get_json().get('date')
        data = Weibo.query.filter_by(date=date).first() 
        if data is None:
            return jsonify({"information":[]}),201
        information = {
                "hotrank":data.hotrank,
                "inflection":data.inflection,
                "proportion":data.proportion,
                }
        return jsonify({"information":information}),200


@api.route('/inflection/trip/province/', methods=['POST'])
def trip_information_province():
    if request.method == 'POST': 
        date = request.get_json().get("date")
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


en_dict = {'安徽': ['31.5', '117.17'], '澳门': ['21.3', '115.07'], '北京': ['39.5', '116.24'], '福建': ['26.0', '119.18'], '甘肃': ['36.0', '103.51'], '广东': ['23.0', '113.14'], '广西': ['22.4', '108.19'], '贵州': ['26.3', '106.42'], '海南': ['20.0', '110.20'], '河北': ['38.0', '114.30'], '河南': ['34.4', '11340'], '黑龙江': ['45.4', '126.36'], '湖北':['30.3', '114.17'], '湖南': ['28.1', '112.59'], '吉林': ['43.5', '125.19'], '江苏': ['32.0', '118.46'], '江西': ['28.4', '115.55'], '辽宁': ['41.4', '123.25'], '内蒙古': ['40.4', '111.41'], '宁夏': ['38.2', '106.16'], '青海': ['36.3', '101.48'], '山东': ['36.4', '117.00'], '山西': ['37.5', '112.33'], '陕西': ['34.1', '108.57'], '上海': ['31.1', '121.29'], '四川': ['30.4', '104.04'], '台湾': ['25.0', '121.30'], '天津': ['39.0', '117.12'], '西藏': ['29.3', '91.08'], '香港': ['21.2', '115.12'], '新疆': ['43.4', '87.36'], '云南': ['25.0', '102.42'], '浙江': ['30.1', '120.10'], '重庆': ['29.3', '106.33']}
