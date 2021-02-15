import datetime
from flask import Blueprint, request, url_for, flash, redirect, jsonify
from util import generate_date_range_from_ls, get_all_lss_per_items, get_all_items, CustomEncoder
import google_auth
import json

api = Blueprint('api', __name__, template_folder='templates')

api_prefix = '/api'

@api.route(f'{api_prefix}/lls', methods=('GET', 'POST'))
@google_auth.authenticated
def get_ls():
    list_items = get_all_items()
    list_ls = get_all_lss_per_items()
    list_date = generate_date_range_from_ls()
    print(list_items)
    #print(json.dumps(list_ls, indent=2))
#    return json.dumps({"items": list_items, "ls": list_ls, "date": list_date}, cls=CustomEncoder)
    return json.dumps(list_date, cls=CustomEncoder)
