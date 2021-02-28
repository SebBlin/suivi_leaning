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
    list_items = get_all_items()
    list_ls = get_all_lss_per_items()
    list_date = generate_date_range_from_ls()
    return json.dumps({"items": list_items, "ls": list_ls, "date": list_date}, indent=2, default=str)
