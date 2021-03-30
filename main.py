import my_stat
from flask import Flask, render_template, request, url_for, flash, redirect, session
import pprint
from util import generate_date_range_from_ls, get_all_lss, get_all_lss_per_items, get_all_items
import json
import os

import learn_session
import google_auth
import api
import diagrams
from secrets import access_secret_version

print(__name__)
app = Flask(__name__)
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False) or access_secret_version(secret_id='FN_FLASK_SECRET_KEY', project_id='979602309341')

app.register_blueprint(learn_session.my_ls)
app.register_blueprint(google_auth.app)
app.register_blueprint(api.api)
app.register_blueprint(diagrams.diagrams)


@app.route('/')
@google_auth.authenticated
def index():
    # Sho all items with Learning session 
    list_items = get_all_items()
    list_ls = get_all_lss_per_items()
    liste_date = generate_date_range_from_ls()
    #print(list_ls)
    print(f'user connected : {session.get("user")}')
    #print(json.dumps(list_ls, indent=2))
    return render_template('index.html', items=list_items, ls=list_ls, date_range=liste_date)

@app.route('/i2')
@google_auth.authenticated
def index2():
    # Sho all items with Learning session 
    list_items = get_all_items()
    list_ls = get_all_lss_per_items()
    liste_date = generate_date_range_from_ls()
    print(list_ls)
    #print(json.dumps(list_ls, indent=2))
    return render_template('index2.html', items=list_items, ls=list_ls, date_range=liste_date)


@app.route('/test')
@google_auth.authenticated
def test():
    liste_date = generate_date_range_from_ls()
    #print(json.dumps(list_ls, indent=2))
    return render_template('test.html', date_range=liste_date)


@app.route('/noauth')
def noauth():
    return render_template('landing_login.html')

@app.route('/plot.png')
def plot_png():
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.use('Agg')

    # Fixing random state for reproducibility
    np.random.seed(19680801)

    mu, sigma = 100, 15
    x = mu + sigma * np.random.randn(10000)

    # the histogram of the data
    n, bins, patches = plt.hist(x, 50, density=True, facecolor='g', alpha=0.75)

    plt.xlabel('Smarts')
    plt.ylabel('Probability')
    plt.title('Histogram of IQ')
    plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
    plt.xlim(40, 160)
    plt.ylim(0, 0.03)
    plt.grid(True)
    fig = plt.figure(1)
    print(fig)
    # draw(ax)
    return my_stat.fig_response(fig)

