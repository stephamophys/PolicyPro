
from dash import Dash, dcc, html, Input, Output, State, callback

app = Dash(__name__)
nsf_icon = './assets/NSF_Official_logo_High_Res_128.png'
app._favicon = 'NSF_Official_logo_High_Res_64.png'

app.layout = html.Div([
    html.Img(src=nsf_icon),
    html.H1(children='NSF Proposal Requirements Checker [DEMO]',
            style={'textAlign':'left', 'font-family':'Papyrus'}),
    dcc.Upload(
        id='upload-file',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
    ),
    html.Div(id='output-file-upload'),
])

def process_file(contents, filename):
    
    print(filename[-3:])
    
    if (filename[-3:] in ['txt', 'htm'] or filename[-4:] == 'html'):
        return html.Div([
            html.H5(filename),
    
            # HTML images accept base64 encoded strings in the same format
            # that is supplied by the upload
            html.H5(children='Processed file.'),
            html.Hr()
        ])
    
    else:
        return html.Div([
            html.H5(filename),
    
            # HTML images accept base64 encoded strings in the same format
            # that is supplied by the upload
            html.H5(children='File type not supported: Must be a plain text or html file'),
            html.Hr()
        ])

@callback(Output('output-file-upload', 'children'),
              Input('upload-file', 'contents'),
              State('upload-file', 'filename'))
def update_output(contents, name):
    if contents is not None:
        children = process_file(contents, name)
        return children

if __name__ == '__main__':
    app.run(debug=True)



'''
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback

import base64
import datetime
import io

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')


    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

if __name__ == '__main__':
    app.run(debug=True)
'''