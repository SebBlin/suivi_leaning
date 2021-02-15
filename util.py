import json
from datetime import timedelta, date
from werkzeug.exceptions import abort

from sqlalchemy import Table, insert, MetaData
import manage_db

import decimal
import json
import sys
import traceback
import types
from datetime import datetime, date


engine = None

def get_db_engine():
    global engine
    engine = engine or manage_db.init_connection_engine()
    conn = manage_db.init_connection_engine()
    return conn

def get_post(post_id):
    global engine
    engine = engine or manage_db.init_connection_engine()
    with engine.connect() as conn:
        post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    if post is None:
        abort(404)
    return post

def get_all_ue():
    global engine
    engine = engine or manage_db.init_connection_engine()
    with engine.connect() as conn:
        ue = conn.execute('SELECT * FROM ues').fetchall()
    return ue

def get_all_college():
    global engine
    engine = engine or manage_db.init_connection_engine()
    with engine.connect() as conn:
        college = conn.execute('SELECT * FROM colleges').fetchall()
    return college

def get_all_items():
    global engine
    engine = engine or manage_db.init_connection_engine()
    with engine.connect() as conn:
        res = conn.execute('SELECT * FROM items').fetchall()
    return res

def get_items(ue):
    global engine
    engine = engine or manage_db.init_connection_engine()
    with engine.connect() as conn:
        rows = conn.execute('SELECT * FROM items WHERE ue_id = ?', (ue,)).fetchall()
    return json.dumps( [dict(ix) for ix in rows] )


def get_all_lss():
    global engine
    engine = engine or manage_db.init_connection_engine()
    with engine.connect() as conn:
        sql = """SELECT  * FROM lss 
            INNER JOIN items 
            INNER JOIN colleges 
            WHERE lss.item_id=items.item_id and lss.college_id=colleges.college_id"""
        res = conn.execute(sql).fetchall()
    return res

def get_all_lss_per_items():
    lss_per_item = {}
    list_item = get_all_lss()
    for item in list_item:
        if item['item_id'] not in lss_per_item.keys():
            lss_per_item[item['item_id']]={}
        lss_per_item[item['item_id']][str(item['date'])]=dict(item)
    return(lss_per_item)

def insert_ls(row):
    print (row)
    global engine
    engine = engine or manage_db.init_connection_engine()
    metadata = MetaData(engine)
    connection = engine.connect()
    lss = Table('lss', metadata, autoload=True, autoload_with=engine)
    ins = insert(lss).values(date=row["date"], college_id=row["college"], item_id=row["item"], serieux=row["serieux"], rang_a=row["rang_a"], rang_b=row["rang_b"])
    res = connection.execute(ins)
    return res


def generate_date_range_from_ls():
    global engine
    engine = engine or manage_db.init_connection_engine()
    with engine.connect() as conn:
        date_ls = conn.execute('SELECT min(date) as datemin, max(date) as datemax FROM lss').fetchone()
        #print(f'date_ls => {date_ls}')
        pdatemin = date.fromisoformat(str(date_ls['datemin']))
        pdatemax = date.fromisoformat(str(date_ls['datemax']))
        nb_days = (pdatemax - pdatemin).days
        r_date = [(pdatemin + timedelta(days=x)).isoformat() for x in range(nb_days+1)]
    return r_date

class CustomEncoder(json.JSONEncoder):
    """
    Internal class used for serialization of types not supported in json.
    """

    def default(self, o):
        if types.FunctionType == type(o):
            return o.__name__
        # sets become lists
        if isinstance(o, set):
            return list(o)
        # date times become strings
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, date):
            return o.isoformat()
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, type):
            return str(o)
        if isinstance(o, Exception):
            return str(o)
        if isinstance(o, set):
            return str(o, 'utf-8')
        if isinstance(o, bytes):
            return str(o, 'utf-8')
        
        return json.JSONEncoder.default(self, o)
