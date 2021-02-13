import sqlite3
import json
from datetime import timedelta, date
from werkzeug.exceptions import abort



def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def get_all_ue():
    conn = get_db_connection()
    ue = conn.execute('SELECT * FROM ues').fetchall()
    conn.close()
    return ue

def get_all_college():
    conn = get_db_connection()
    college = conn.execute('SELECT * FROM colleges').fetchall()
    conn.close()
    return college

def get_all_items():
    conn = get_db_connection()
    res = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return res

def get_items(ue):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    print ('select for ue', ue)
    rows = conn.execute('SELECT * FROM items WHERE ue_id = ?', (ue,)).fetchall()
    conn.close()
    return json.dumps( [dict(ix) for ix in rows] )


def get_all_lss():
    conn = get_db_connection()
    sql = """
        SELECT  * FROM lss 
        INNER JOIN items 
        INNER JOIN colleges 
        WHERE lss.item_id==items.item_id and lss.college_id == colleges.college_id
        """

    res = conn.execute(sql).fetchall()
    conn.close()
    return res

def get_all_lss_per_items():
    lss_per_item = {}
    list_item = get_all_lss()
    for item in list_item:
        if item['item_id'] not in lss_per_item.keys():
            lss_per_item[item['item_id']]={}
        lss_per_item[item['item_id']][item['date']]=dict(item)
    return(lss_per_item)

def generate_date_range_from_ls():
    conn = get_db_connection()
    date_ls = conn.execute('SELECT min(date) as datemin, max(date) as datemax FROM lss').fetchone()
    pdatemin = date.fromisoformat(date_ls['datemin'])
    pdatemax = date.fromisoformat(date_ls['datemax'])
    nb_days = (pdatemax - pdatemin).days
    r_date = [(pdatemin + timedelta(days=x)).isoformat() for x in range(nb_days+1)]
    conn.close()
    return r_date
