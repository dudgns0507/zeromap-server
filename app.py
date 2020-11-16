import json
import os

from flask import Flask, render_template, request
from flask_marshmallow import Marshmallow

from flaskext.mysql import MySQL
from sqlalchemy import and_, func, asc, or_, any_

import models.models as mo
from models.models import *
from models.Util import add, commit, delete

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_pyfile('config.py')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['TEMPLATES_AUTO_RELOAD'] = True

mysql = MySQL()
ma = Marshmallow(app)

mysql.init_app(app)
mo.init_app(app)


def dump(obj):
    return json.dumps(obj, ensure_ascii=False)


@app.route('/')
def hello_world():
    log = Log()
    log.ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    add(db.session, log)

    return render_template('index.html')


@app.route('/api/store', methods=['POST'])
def api_store():
    lng = request.form.get('lng', 0)
    lat = request.form.get('lat', 0)

    store = Store.query \
        .filter(and_(Store.lng != 0, Store.lat != 0)) \
        .filter((func.acos(
                    func.sin(func.radians(lat)) * func.sin(func.radians(Store.lat)) + func.cos(func.radians(lat)) * func.cos(
                        func.radians(Store.lat)) * func.cos(func.radians(Store.lng) - (func.radians(lng)))) * 6371) < 0.5) \
        .order_by(asc((func.acos(
                    func.sin(func.radians(lat)) * func.sin(func.radians(Store.lat)) + func.cos(func.radians(lat)) * func.cos(
                        func.radians(Store.lat)) * func.cos(func.radians(Store.lng) - (func.radians(lng)))) * 6371))) \
        .limit(100)

    result = {
        "code": 200,
        "message": "success",
        "stores": StoreSchema(many=True).dump(store)
    }

    return dump(result)


@app.route('/api/search/store', methods=['POST'])
def api_search_store():
    category_list = ["카페", "편의점/마트", "음식점", "디저트", "병원/약국", "의류"]
    list = [
        ["비알코올 음료점업"],
        ["음ㆍ식료품 위주 종합 소매업", "식료품 소매업", "서적 및 문구용품 소매업", "신선 식품 및 단순 가공 식품 도매업"],
        ["한식 음식점업", "외국식 음식점업", "기타 간이 음식점업", "주점업"],
        ["떡, 빵 및 과자류 제조업"],
        ["수의업", "병원", "의약품, 의료%", "의원"],
        ["의복 소매업"],
    ]
    q = request.form.get('q', '')
    c = request.form.getlist('c[]')
    lng = request.form.get('lng', 0)
    lat = request.form.get('lat', 0)

    qArr = q.split(' ')
    cArr = []

    if len(c) > 0 and c[0] == "전체":
        cArr.append("%%")
    elif len(c) == 0:
        cArr.append("")
    else:
        for i in range(0, len(c)):
            try:
                type = category_list.index(c[i])
            except ValueError:
                continue

            for j in range(0, len(list[type])):
                cArr.append(list[type][j])

    for i in range(0, len(qArr)):
        qArr[i] = "%" + qArr[i] + "%"

    store = Store.query \
        .filter(and_(Store.lng != 0, Store.lat != 0)) \
        .filter((func.acos(
                    func.sin(func.radians(lat)) * func.sin(func.radians(Store.lat)) + func.cos(func.radians(lat)) * func.cos(
                        func.radians(Store.lat)) * func.cos(func.radians(Store.lng) - (func.radians(lng)))) * 6371) < 0.5) \
        .order_by(asc((func.acos(
                    func.sin(func.radians(lat)) * func.sin(func.radians(Store.lat)) + func.cos(func.radians(lat)) * func.cos(
                        func.radians(Store.lat)) * func.cos(func.radians(Store.lng) - (func.radians(lng)))) * 6371))) \
        .filter(or_(or_(*[Store.name.like(name) for name in qArr]), or_(*[Store.category.like(name) for name in qArr]))) \
        .filter(or_(*[Store.category.like(name) for name in cArr])) \
        .limit(100)

    result = {
        "code": 200,
        "message": "success",
        "stores": StoreSchema(many=True).dump(store)
    }
    return dump(result)


@app.route('/api/report', methods=['POST'])
def api_report():
    id = request.form.get('id', 0)
    title = request.form.get('title', '')
    text = request.form.get('text', '')

    report = Report()
    report.store = id
    report.log = title
    report.text = text

    add(db.session, report)

    result = {
        "code": 200,
        "message": "success"
    }

    return dump(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
