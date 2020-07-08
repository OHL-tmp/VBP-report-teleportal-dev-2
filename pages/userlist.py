import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import time

import datetime
import json
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output, State

from app import app

app = dash.Dash(__name__, url_base_pathname='/login/')

server = app.server


def create_layout(app):
	
	return html.Div(
                [
                    dbc.Input(type="text", id='number-input'),
                    html.Div(
                        [
                            html.Div(id='live-update-text'),
                            
                            dcc.Interval(
                                id='interval-component',
                                interval=100*1000, # in milliseconds
                                n_intervals=0
                            )
                        ]
                    )
                ],
                # style={"margin-top":"-30rem","background-color":"transparent","text-align":"center"}
            )


app.layout = create_layout(app)


@app.callback(Output('live-update-text', 'children'),
            [
              Input('interval-component', 'n_intervals'),
              Input("number-input", "value")
            ]
            )
def update_metrics(n, value):
    style = style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}

    itemlist = []

    if value:
        value = int(value)
        for i in range(value):
            layout = html.Div(
                        html.H2(str(i)),
                        style = style
                    )
            itemlist.append(layout)

    else:
        itemlist

    return itemlist


if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True,port=8053)