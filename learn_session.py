import datetime
from flask import Blueprint, render_template, request, url_for, flash, redirect, session
from util import get_all_items, get_all_ue, get_all_college, get_all_lss, get_all_items, get_items, insert_ls
import google_auth

import pprint

my_ls = Blueprint('learning_session', __name__, template_folder='templates')

ls_prefix = '/ls'
ls_filename = 'ls.csv'
lc_filename = 'list_college.csv'

@my_ls.route(f'{ls_prefix}/create', methods=('GET', 'POST'))
@google_auth.authenticated
def create():
    if request.method == 'POST':
        new_row = {'day':       request.form.get('day'),
                    'month':    request.form.get('month'),
                    'year':     request.form.get('year'),
                    'date':     datetime.date(year=int(request.form.get('year')), month=int(request.form.get('month')), day=int(request.form.get('day'))).strftime("%Y-%m-%d"),
                    'ue':       request.form.get('selectue'),
                    'college':  request.form.get('college'),
                    'item':     request.form.get('item'),
                    'serieux':  request.form.get('serieux'),
                    'rang_a':   True if request.form.get('rang_a') else False,
                    'rang_b':   True if request.form.get('rang_b') else False,
                   }
        pprint.pprint(new_row)
        res = insert_ls(new_row, session['user'])
        if res:
            flash('Nouvelle session enregistrée!', category='info')
        else:
            flash('Erreur d''enregistrement de session!')
        return redirect(url_for('learning_session.index'))
    else:
        ues = get_all_ue()
        colleges = get_all_college()
        items = get_all_items()
        print(items)
        return render_template('ls/create.html', ues=ues, colleges=colleges, items=items)

@my_ls.route(f'{ls_prefix}/', methods=('GET', ))
@google_auth.authenticated
def index():
    lss = get_all_lss()
    return render_template('ls/index.html', row_data=lss)


@my_ls.route(f'{ls_prefix}/get-items-for-ue', methods=('POST', ))
@google_auth.authenticated
def get_list_items_for_ue():
    list_items = []
    if request.method == 'POST':
        ue = request.form.get('ue')
        if ue:
            list_items = get_items(ue)
            print ('items for ue', list_items)
    return list_items


