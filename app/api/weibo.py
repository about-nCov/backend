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


@api.route('/inflection/weibo/proportion/', methods=['GET'])
def weibo_proportion():
    if request.method == "GET":
        date = request.get_json().get('date')
        date = date_limiter(date, '/', 0)
        data = Weibo.query.filter_by(date=date).first()
        if data is None:
            return jsonify({"information":[]}),201
        information = {
                "hotrank":data.hotrank,
                "inflection":data.inflection,
                "proportion":data.proportion,
                }
        return jsonify({"information":information}),200


