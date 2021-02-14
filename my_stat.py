# list of variables 
import io
import pandas as pd
import os
from flask import send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

ue_file_name = "list_ue.csv"


def get_all_ue():
    print(os.getcwd())
    df_ue = pd.read_csv(ue_file_name, sep=';')
    return df_ue


if __name__ == "__main__":
    # execute only if run as a script
    res = get_all_ue()
    print(res)


## gestion des images 

def fig_response(fig):
    """Turn a matplotlib Figure into Flask response"""
    img_bytes = io.BytesIO()
    fig.savefig(img_bytes)
    img_bytes.seek(0)
    return send_file(img_bytes, mimetype='image/png')