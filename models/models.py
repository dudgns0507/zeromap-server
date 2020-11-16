# -*- coding: utf-8 -*-
from flask_marshmallow import Schema
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from sqlalchemy import Column, Text, Integer, DateTime, FetchedValue

db = SQLAlchemy()


class Store(db.Model):
    __tablename__ = 'store'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    no = db.Column(db.Text)
    mest_no = db.Column(db.Text)
    main_area = db.Column(db.Text)
    area = db.Column(db.Text)
    name = db.Column(db.Text)
    category = db.Column(db.Text)
    type = db.Column(db.Text)
    address = db.Column(db.Text)
    address_detail = db.Column(db.Text)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    report = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, server_default=FetchedValue())


class StoreSchema(Schema):
    class Meta:
        fields = (
            "id",
            "no",
            "mest_no",
            "main_area",
            "area",
            "name",
            "category",
            "type",
            "address",
            "address_detail",
            "lng",
            "lat",
            "report",
            "created_date"
        )


class Report(db.Model):
    __tablename__ = 'report'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    store = db.Column(db.Integer)
    log = db.Column(db.Text)
    text = db.Column(db.Text)
    created_date = db.Column(db.DateTime, server_default=FetchedValue())


class ReportSchema(Schema):
    class Meta:
        fields = (
            "id",
            "store",
            "log",
            "text",
            "created_date"
        )


class Log(db.Model):
    __tablename__ = 'log'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    ip = db.Column(db.Text)
    created_date = db.Column(db.DateTime, server_default=FetchedValue())


class LogSchema(Schema):
    class Meta:
        fields = (
            "id",
            "ip",
            "created_date"
        )


def init_app(app):
    db.init_app(app)
