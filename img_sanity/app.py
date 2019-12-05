import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_table

import pandas as pd
import base64
from os import path
import argparse
import flask


def encode_image(name):
    return base64.b64encode(open(name, 'rb').read())

def decode_image(name):
    encoded_image = encode_image(name)
    return 'data:image/png;base64,{}'.format(encoded_image.decode())

parser = argparse.ArgumentParser(
    description='An interactive image filter.'
)
parser.add_argument(
    'table', metavar='table', type=str,
    help='The name of the table storing image attributes and names'
)
parser.add_argument(
    '--img_column', default='name', type=str,
    help='The column that stores the image file names'
)
parser.add_argument(
    '--img_path', default='', type=str,
    help='The path to the images. It is joined with the values in img_column'
)

args = parser.parse_args()
file = args.table
img_column = args.img_column
img_path = args.img_path
img_path = path.abspath(img_path)
static_image_route = '/static/'

df = pd.read_csv(file)

list_of_images = [name for name in df[img_column]]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# external_stylesheets = [dbc.themes.BOOTSTRAP]
# app = dash.Dash()
app = dash.Dash(
    __name__, external_stylesheets=external_stylesheets
)
server = app.server

app.layout = html.Div([
    html.H1('Image Filter'),

    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i, "deletable": False} for i in df.columns],
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        page_action="native",
        page_current=0,
        page_size=7,
        sort_mode="multi",
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
        ],
        style_table={
            'height': '290px',
            'overflowY': 'scroll',
            'border-bottom': 'thin lightgrey solid'
        }
    ),

    html.Div(id='img-grid', className='row',
             # style={"maxHeight": "500px", "overflow": "scroll"}
             # style={'flex': '1 1 auto', 'overflow': 'scroll'}
             ),
],
# style={'height': '100%', 'display': 'flex', 'flex-flow': 'column'}
)


@app.callback(
    Output("img-grid", "children"),
    [Input("table", "derived_virtual_data")]
)
def show_images(rows):
    if rows is None:
        _df = df
    else:
        _df = pd.DataFrame(rows)

    images = [
        # html.Img(src=decode_image(path.join(img_path, name)))
        html.Img(src=path.join(static_image_route, name))
        for name in _df[img_column]
        ]
    return images


# Add a static image route that serves images from desktop
# Be *very* careful here - you don't want to serve arbitrary files
# from your computer or server
@app.server.route(path.join(static_image_route, '<image_name>'))
def serve_image(image_name):
    if image_name not in list_of_images:
        raise Exception('"{}" is excluded from the allowed static files'.format(image_name))
    return flask.send_from_directory(img_path, image_name)


if __name__ == '__main__':
    app.run_server(debug=True)
