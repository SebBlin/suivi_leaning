# modules to create diagrames 
import flask
import io
import json

from flask import send_file, render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import bokeh
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.embed import json_item
from bokeh.palettes import Spectral6
from bokeh.transform import factor_cmap

from bokeh.sampledata.iris import flowers
import pandas as pd

from util import df_from_sql

uri_prefix = '/diagrams'

diagrams = flask.Blueprint('digrams', __name__)



colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
colors = [colormap[x] for x in flowers['species']]

def make_plot(x, y):
    p = figure(title = "Iris Morphology", sizing_mode="fixed", plot_width=800, plot_height=400)
    p.xaxis.axis_label = x
    p.yaxis.axis_label = y
    p.circle(flowers[x], flowers[y], color=colors, fill_alpha=0.2, size=10)
    return p

@diagrams.route(f'{uri_prefix}/')
def root():
    
    print (render_template('diagrams/root.html',resources=CDN.render(), prefix=uri_prefix))
    return render_template('diagrams/root.html',resources=CDN.render(), prefix=uri_prefix)

@diagrams.route(f'{uri_prefix}/plot')
def plot():
    
    sql= """SELECT * FROM items
            LEFT JOIN 
            (SELECT  item_id, college_id,  AVG(mlss.age) as avg_age, AVG(mlss.serieux) as avg_serieux, COUNT(id) as nb_item FROM 
                (SELECT id, item_id, college_id,  serieux, DATEDIFF(CURDATE(), `date`) as age from lss) as mlss
            GROUP BY item_id, college_id) AS item_synt
            ON items.item_id = item_synt.item_id
            LEFT JOIN colleges
            ON item_synt.college_id = colleges.college_id ;
            """
    df = df_from_sql(sql)
    df = df.loc[:,~df.columns.duplicated()]
    df['size']=df['nb_item']*12

    TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"
    TOOLTIPS = [
        ("item", "@item_name"),
        ("College","@college_name"),
        ("Nb essions", "@nb_item"),
    ]
    p = figure(tools=TOOLS, title = "Items", sizing_mode="scale_both", plot_width=100, plot_height=50, tooltips=TOOLTIPS)
    p.xaxis.axis_label = 'Serieux'
    p.yaxis.axis_label = 'Age'
    p.y_range.flipped = True

    mapper = factor_cmap(field_name='college_id', factors=df['college_id'].dropna().values, palette=Spectral6)
    print(df['college_id'].dropna().unique())
    p.circle('avg_serieux', 'avg_age',source=df, color=mapper, size="size", fill_alpha=0.4, legend_field="college_name")
    p.legend.location = "top_left"
    p.legend.click_policy="hide"
    return json.dumps(json_item(p, "myplot"))












@diagrams.route(f'{uri_prefix}/basic.png')
def basic():
    plot = figure()
    plot.circle([1,2], [3,4])

    return file_html(plot, CDN, "my plot")


@diagrams.route(f'{uri_prefix}/plot.png')
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
    return fig_response(fig)

def fig_response(fig):
    """Turn a matplotlib Figure into Flask response"""
    img_bytes = io.BytesIO()
    fig.savefig(img_bytes)
    img_bytes.seek(0)
    return send_file(img_bytes, mimetype='image/png')