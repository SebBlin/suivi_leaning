import datetime
from flask import Blueprint, request, url_for, flash, redirect, jsonify
from util import generate_date_range_from_ls, get_all_lss_per_items, get_all_items, cvt_to_dict
import google_auth
import json

api = Blueprint('api', __name__, template_folder='templates')

api_prefix = '/api'

@api.route(f'{api_prefix}/lls', methods=('GET', 'POST'))
#@google_auth.authenticated
def get_ls():
    list_items = get_all_items()[:20]
    list_ls = get_all_lss_per_items()
    list_date = generate_date_range_from_ls()
    #columns = ['#items'].extend(array(list_date))
    columns = ['#', 'items']
    columns.extend(list_date)

    data = []
    for num, item in enumerate(list_items, start=1):
        row = [item[0], item[2]]
        if list_ls.get(num):
            ilss = list_ls.get(num)
            for d in list_date:
                row.append('x' if d in ilss.keys() else '')
        else:
            row.extend([''] * len(list_date))
        data.append(row)

    resp = {
        "data": data
    }
    return json.dumps(resp, default=str)
    return json.dumps(resp, indent=2, default=str)

@api.route(f'{api_prefix}/cols', methods=('GET', 'POST'))
#@google_auth.authenticated
def get_cols():
    list_date = generate_date_range_from_ls()
    columns = ['#', 'items']
    columns.extend(list_date)
    return json.dumps(columns, default=str)
    return json.dumps(resp, indent=2, default=str)
