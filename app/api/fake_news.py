# coding:utf-8
import json
import time
from . import api
from app import db
from app.models import FakeNews
from flask import jsonify, request, Response


@api.route('/inflection/fake_news/', methods=['GET'])
def fake_news():
    if request.method == "GET":
        datas = FakeNews.query.limit(50)
        if datas is None:
            return jsonify({"information":[]}),201
        information_list = []
        for data in datas:
            information = {
                    "title":data.title,
                    "mainSummary":data.mainSummary,
                    "body":data.body,
                    "time":data.time
                    }
            information_list.append(information)
        return jsonify({"information":information_list}),200


