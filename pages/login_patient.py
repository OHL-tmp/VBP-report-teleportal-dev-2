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

username = "demo-patient"
password = "demo2020"

def login_layout(app):
	
	return html.Div(
                [
                    html.Div(
                    	[
                            html.Div(
                                html.Img(src=app.get_asset_url("coeus.png"),style={"height":"4rem"}),
                                style={"text-align":"center","padding":"4rem"}
                            ),
                            html.Div(
                                html.H2("Patient",style={"font-size":"1.6rem","padding-left":"20px"}),
                                style={"text-align":"start"}
                            ),
                            html.Div(id = 'store-location'),
                        	dbc.Card(
                        		dbc.CardBody(
                        			[	
                                        html.Div(style={"padding-top":"20px"}),
                                        dbc.Collapse(children = ["\u2757", "Please check your username and password."],
                                            id = 'login-collapse-check',
                                            is_open = False,
                                            style={"text-align":"center"}
                                            ),
                        				html.Div(
                        					dbc.Input(placeholder="Username", type="text", style={"border-radius":"10rem"}, id = "login-input-username"),
                        					style={"padding":"0.5rem"}
                        				),
                        				html.Div(
                        					dbc.Input(placeholder="Password", style={"border-radius":"10rem"}, type = 'password', id = "login-input-password"),
                        					style={"padding":"0.5rem"}
                        				),
                        				dbc.Row(
                        					[
                        						dbc.Col(
                        							html.Div(),
                        						),
                        						dbc.Col(
                        							[
                        								dbc.Button(
										                    "Log In",
										                    # id = 'manager-button-openmodal-pmpm',
										                    className="mb-3",
										                    style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"1rem","width":"6rem"},
                                                            id = "login-button-submit"
										                ),
                        							],
                        							width=3
                        						),
                                                dbc.Col(
                                                    html.Div(),
                                                ),
                        					],
                        					style={"padding-top":"2rem", "padding-right":"1rem"}
                        				)
                        			],
                                    style={"padding-left":"2rem","padding-right":"2rem"}
                        		),
				                className="mb-3",
				                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.1), 0 6px 20px 0 rgba(0, 0, 0, 0.1)", "border":"2px solid #1357dd", "border-radius":"1rem"}
                        	)
                    	],
                    style={"background-color":"transparent", "border":"none", "width":"500px", "margin":"auto", "padding-top":"10vh"}
                    ),
                ],
                style={"background":"url(./assets/patient-login.png)","height":"100vh"}
            )


app.layout = login_layout(app)


@app.callback(
    [Output("login-collapse-check", "is_open"),
#    Output("login-button-submit", "href")
    Output("store-location", "children")],
    [Input("login-button-submit", "n_clicks")],
    [State("login-input-username", "value"),
    State("login-input-password", "value")]
    )
def login_cjeck(n, un, pw):
    if n:
        if un == username and pw == password:
            return False, dcc.Location(pathname = "/patient/", id='login-success')
        else: 
            return True, ""
    else: 
        return False, ""

if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True,port=8052)