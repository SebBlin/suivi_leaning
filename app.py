import my_stat
from flask import Flask, render_template, request, url_for, flash, redirect
import pprint
from util import generate_date_range_from_ls, get_all_lss, get_all_lss_per_items, get_db_connection, get_all_items
import json
import os

import learn_session
import google_auth

print(__name__)
app = Flask(__name__)
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.register_blueprint(learn_session.my_ls)
app.register_blueprint(google_auth.app)

@app.route('/')
@google_auth.authenticated
def index():
    # Sho all items with Learning session 
    list_items = get_all_items()
    list_ls = get_all_lss_per_items()
    liste_date = generate_date_range_from_ls()
    print(json.dumps(list_ls, indent=2))
    return render_template('index.html', items=list_items, ls=list_ls, date_range=liste_date)

@app.route('/noauth')
def noauth():
    return render_template('landing_login.html')


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        pprint.pprint(request)
        title = request.form['title']
        content = request.form['content']
 
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))
 

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

