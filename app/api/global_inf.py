# coding:utf-8
import json
from . import api
from app import db
from app.models import World
from flask import jsonify, request, Response



@api.route('/inflection/global/', methods=['GET'])
def global_information():
    if request.method == 'GET':
        all_data = World.query.all()    
        information_list = []
        if all_data is None:
            return jsonify({"information": {}}), 201
        for data in all_data:
            information = {"continentName": data.continentName,
                           "country": data.countryName,
                           "confirmed": data.confirmedCount,
                           "death": data.deadCount,
                           "cured": data.curedCount,
                           }
            information_list.append(information)
        return jsonify({"information_list":information_list}),200
