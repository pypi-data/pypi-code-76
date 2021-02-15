import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
from pathlib import Path
from pyhard.utils import reduce_dim

_my_path = Path(__file__).parent
_folder = 'overlap'
datadir = _my_path.parents[1] / 'data'
list_dir = [x.name for x in datadir.glob('**/*') if x.is_dir()]
list_dir.sort()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df2 = pd.DataFrame({'A': [1, 1, 2, 2, 1.5, 1.5], 'B': [1, 2, 1, 2, 1, 2], 'C': [1, 2, 3, 4, 5, 6],
                    'D': ['a', 'b', 'c', 'd', 'e', 'f'], 'long_name_blabla': [0, 1, 0, 1, 0, 1]})
df2.index.name = 'n'
df2.reset_index(inplace=True)

colors = {
    'background': '#292929',
    'text': 'rgb(55, 83, 109)',
    'blue': 'rgb(26, 118, 255)'
}

app.layout = html.Div([
    html.H3('Instance Hardness Dashboard', style={'color': colors['blue']}),
    html.Div([
        html.Div([
            html.H4('Options', style={'color': colors['text']}),
            html.Div([
                html.H5('Dataset', style={'color': colors['text']}),
                dcc.Dropdown(
                    id='data',
                    options=[{'label': i, 'value': i} for i in list_dir],
                    value='overlap',
                    clearable=False
                ),
                html.Br(),
                html.H5('Color', style={'color': colors['text']}),
                dcc.Dropdown(
                    id='color',
                    options=[{'label': i, 'value': i} for i in df2.columns],
                    value='C',
                    clearable=False
                ),
                html.Br(),
                html.H6('Color Bar', style={'color': colors['text']}),
                dcc.Checklist(
                    id='manual',
                    options=[{'label': 'Manual', 'value': 'on'}],
                    value=[],
                    style={'margin-left': 20, 'margin-bottom': 10, 'color': colors['text']}
                ),
                # html.Br(),
                dcc.RangeSlider(
                    id='colorbar-range',
                    count=0,
                    min=-40,
                    max=40,
                    step=1,
                    value=[-20, 20],
                    updatemode='drag',
                    allowCross=False
                ),
                # html.Div(id='slider-value', style={'margin-top': 0, 'margin-left': 20})
                # html.Br(),
            ], style={'margin-top': 30})],
            # style={'width': '16%', 'display': 'inline-block', 'margin-left': '0px',
            #        'margin-right': '0px', 'float': 'left'},
            # 'backgroundColor': '#E0E0E0'
            style={'width': '18%'},
            className="three columns"
        ),

        html.Div([
            dcc.Graph(id='g1')
        ],
            # style={'width': '40%', 'display': 'inline-block', 'float': 'left'},
            style={'margin-left': 20, 'margin-right': 0},
            className="five columns"
        ),

        html.Div([
            dcc.Graph(id='g2')
        ],
            # style={'width': '40%', 'display': 'inline-block', 'float': 'left', 'margin': '0'},
            style={'margin-left': 5, 'margin-right': 0},
            className="five columns"
        ),
    ], className="row"),
    # html.H5("Hover", style={'color': colors['text']}),
    # dcc.Dropdown(
    #     options=[{'label': i, 'value': i} for i in df2.columns],
    #     multi=True,
    #     value='')
    html.Div(id='temp'),
    html.Div(id='storage', style={'display': 'none'}),
    html.Div(id='keys', style={'display': 'none'})
],  # style={'height': '100%', 'top': '0px'}
)


@app.callback([Output('storage', 'children'),
               Output('keys', 'children')],
              [Input('data', 'value')])
def load_data(folder):
    dim_method = 'LDA'
    folder = datadir / folder
    dataset = pd.read_csv(folder / 'data.csv')

    if len(dataset.columns) > 3:
        X = dataset.iloc[:, :-1]
        y = dataset.iloc[:, -1]
        X_embedded = reduce_dim(X, y, method=dim_method)
        df = pd.DataFrame(X_embedded, columns=['V1', 'V2'], index=X.index)
        dataset = pd.concat([df, y], axis=1)

    df_metadata = pd.read_csv(folder / 'metadata.csv', index_col='instances')
    df_is = pd.read_csv(folder / 'coordinates.csv', index_col='Row')
    df_is.index.name = 'instances'

    dataset.index = df_metadata.index
    df_data = df_is.join(dataset)
    df_data = df_data.join(df_metadata)
    df_data.index = df_data.index.map(str)

    data_cols = dataset.columns.to_list()
    is_cols = df_is.columns.to_list()
    keys_dict = dict(is_kdims=is_cols[0:2],
                     data_dims=dataset.columns.to_list(),
                     data_kdims=data_cols[0:2],
                     class_label=data_cols[2],
                     meta_dims=df_metadata.columns.to_list())

    return df_data.to_json(date_format='iso', orient='split'), json.dumps(keys_dict)


@app.callback(Output('colorbar-range', 'marks'),
              [Input('colorbar-range', 'value')])
def bar_callback(value):
    return {0: '', value[0]: '{0}'.format(value[0]), value[1]: '{0}'.format(value[1])}


def convert_json(df_json, keys_json):
    return pd.read_json(df_json, orient='split'), json.loads(keys_json)


@app.callback([Output('g1', 'figure'),
               Output('g2', 'figure'),
               Output('temp', 'children')],
              [Input('g1', 'selectedData'),
               Input('g2', 'selectedData'),
               Input('color', 'value'),
               Input('colorbar-range', 'value'),
               Input('manual', 'value')],
              state=[State('storage', 'children'),
                     State('keys', 'children')])
def selection_callback(selection1, selection2, color, color_range, manual_range, df_json, keys_json):
    df, keys = convert_json(df_json, keys_json)
    selectedpoints = df.index
    for selected_data in [selection1, selection2]:
        if selected_data and selected_data['points']:
            selectedpoints = np.intersect1d(selectedpoints, [p['customdata'] for p in selected_data['points']])

    if not manual_range:
        color_range = None

    fig1 = px.scatter(df, x=df[keys['data_kdims'][0]], y=df[keys['data_kdims'][1]],
                      color=keys['class_label'], hover_name=df[keys['class_label']],
                      color_continuous_scale='Bluered',
                      height=450, title='Original Data',
                      range_color=color_range, custom_data=[df.index])
    fig1.update_traces(selectedpoints=selectedpoints)  # customdata=df.index,
    fig1['layout']['uirevision'] = 'constant'

    fig2 = px.scatter(df, x=df[keys['is_kdims'][0]], y=df[keys['is_kdims'][1]],
                      color=keys['class_label'], hover_name=df[keys['class_label']],
                      color_continuous_scale='Bluered',
                      height=450, title='Instance Space',
                      range_color=color_range, custom_data=[df.index])
    fig2.update_traces(customdata=df.index, selectedpoints=selectedpoints)
    # fig2.update(layout_coloraxis_showscale=False)
    fig2['layout']['uirevision'] = 'constant'

    fig1.update_layout(margin={'l': 0, 'r': 0, 't': 80, 'b': 0},
                       title_font_family='HelveticaNeue',
                       font_family='HelveticaNeue',
                       font_color=colors['text'],
                       dragmode='lasso')
    fig2.update_layout(margin={'l': 0, 'r': 0, 't': 80, 'b': 0},
                       title_font_family='HelveticaNeue',
                       font_family='HelveticaNeue',
                       font_color=colors['text'],
                       dragmode='lasso')

    # fig1['layout']['plot_bgcolor'] = colors['background']
    # fig1['layout']['paper_bgcolor'] = colors['background']

    return fig1, fig2, selection1


if __name__ == '__main__':
    app.run_server(debug=True)
