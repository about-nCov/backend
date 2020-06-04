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
        date = date_limiter(date, '.', 1)
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

#en_dict = {'安徽': ['31.5', '117.17'], '澳门': ['21.3', '115.07'], '北京': ['39.5', '116.24'], '福建': ['26.0', '119.18'], '甘肃': ['36.0', '103.51'], '广东': ['23.0', '113.14'], '广西': ['22.4', '108.19'], '贵州': ['26.3', '106.42'], '海南': ['20.0', '110.20'], '河北': ['38.0', '114.30'], '河南': ['34.4', '11340'], '黑龙江': ['45.4', '126.36'], '湖北':['30.3', '114.17'], '湖南': ['28.1', '112.59'], '吉林': ['43.5', '125.19'], '江苏': ['32.0', '118.46'], '江西': ['28.4', '115.55'], '辽宁': ['41.4', '123.25'], '内蒙古': ['40.4', '111.41'], '宁夏': ['38.2', '106.16'], '青海': ['36.3', '101.48'], '山东': ['36.4', '117.00'], '山西': ['37.5', '112.33'], '陕西': ['34.1', '108.57'], '上海': ['31.1', '121.29'], '四川': ['30.4', '104.04'], '台湾': ['25.0', '121.30'], '天津': ['39.0', '117.12'], '西藏': ['29.3', '91.08'], '香港': ['21.2', '115.12'], '新疆': ['43.4', '87.36'], '云南': ['25.0', '102.42'], '浙江': ['30.1', '120.10'], '重庆': ['29.3', '106.33']}

en_dict = { '黑龙江': [127.9688, 45.368],
            '内蒙古': [110.3467, 41.4899],
            "吉林": [125.8154, 44.2584],
            '北京': [116.4551, 40.2539],
            "辽宁": [123.1238, 42.1216],
            "河北": [114.4995, 38.1006],
            "天津": [117.4219, 39.4189],
            "山西": [112.3352, 37.9413],
            "陕西": [109.1162, 34.2004],
            "甘肃": [103.5901, 36.3043],
            "宁夏": [106.3586, 38.1775],
            "青海": [101.4038, 36.8207],
            "新疆": [87.9236, 43.5883],
            "新疆维吾尔自治区": [87.9236, 43.5883],
            "西藏": [91.11, 29.97],
            "四川": [103.9526, 30.7617],
            "重庆": [108.384366, 30.439702],
            "山东": [117.1582, 36.8701],
            "河南": [113.4668, 34.6234],
            "江苏": [118.8062, 31.9208],
            "安徽": [117.29, 32.0581],
            "湖北": [114.3896, 30.6628],
            "浙江": [119.5313, 29.8773],
            "福建": [119.4543, 25.9222],
            "江西": [116.0046, 28.6633],
            "湖南": [113.0823, 28.2568],
            "贵州": [106.6992, 26.7682],
            "云南": [102.9199, 25.4663],
            "广东": [113.12244, 23.009505],
            "广西": [108.479, 23.1152],
            "广西壮族自治区": [108.479, 23.1152],
            "海南": [110.3893, 19.8516],
            '上海': [121.4648, 31.2891]}
