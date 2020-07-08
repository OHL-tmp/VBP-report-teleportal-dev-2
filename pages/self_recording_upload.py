import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

import pandas as pd
import numpy as np

import pathlib
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
from server import app, server


def modal_self_recording(app):
    return html.Div(
            [
                html.H6("Entry", style={"font-size":"0.7rem","padding-top":"10px"}),
                dbc.Button(children = [html.Img(src=app.get_asset_url("icon-upload-to-the-cloud-100.png"), style={"height":"1.5rem", "padding-top":"0px"})], color="light",style={"border-radius":"10rem"}, id = 'video-modal-upload-button-open'),
                dbc.Modal(
                    [
                        dbc.ModalHeader(
                            [
                                html.H1("Berg Balance Scale",style={"font-size":"1.2rem","padding-bottom":"10px"}),
                                html.Div(
                                    [
                                        html.H2("Instruction: Please perform the following 14 tasks and record in one video to upload:",style={"font-size":"0.8rem"}),
                                        html.H6("1. Please stand up from sitting position. Try not to use your hands for support"),
                                        html.H6("2. Stand for 2 minutes without holding"),
                                        html.H6("3. Please sit down from standing position"),
                                        html.H6("4. Sit with arms folded for 2 minutes"),
                                        html.H6("5. Place your feet together and stand without holding"),
                                        html.H6("6. Close your eyes and stand still for 10 seconds"),
                                        html.H6("7. Please move from chair or bed and back again"),
                                        html.H6("8. Lift arm to 90 degrees. Stretch out your fingers and reach forward as far as you can"),
                                        html.H6("9. Pick up the shoe which is placed in front of your feet"),
                                        html.H6("10. Turn to look behind you over your left shoulder, repeat to the right"),
                                        html.H6("11. Turn completely around in a full circle. Pause. Then turn a full circle in the other direction"),
                                        html.H6("12. Place each foot alternately on the stool. Continue until each foot has touched the stool 4 times"),
                                        html.H6("13. Place one foot directly in front of the other"),
                                        html.H6("14. Stand on one leg as long as you can without holding"),
                                    ],
                                    style={"border-radius":"0.5rem","background":"#f5f5f5","padding":"20px"}
                                ),
                            ],
                            style={"padding":"40px","wdith":"100%"}
                        ),
                        dbc.ModalBody(video_modal_upload_body(), style={"padding":"40px"}),
                        dbc.ModalFooter(
                            dbc.Button("Submit", id="video-modal-upload-button-submit", className="mr-2",style={"width":"160px"}),
                            style={"padding-right":"42%"}
                        )
                    ],
                    id = "modal-selfrecording-upload",
                    size = 'xl',
                    backdrop = "static"
                )
            ],
            style={"text-align":"center"}
        )

def video_modal_upload_body():
    return html.Div([
            dcc.Upload(
                id = 'video-modal-upload-upload',
                children = html.Div([
                    'Select Related Video to Upload'
                    ],style={"font-family":"NotoSans-Regular","font-size":"0.8rem","text-decoration":"underline","color":"#1357DD"}),
                style={
                    'height': '40px',
                    'lineHeight': '40px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center'
                    },
                accept = "video/*"
                ),
            html.Div(id = "video-modal-upload-output",style={"margin-top":"20px","padding":"20px","background":"#f5f5f5","border-radius":"0.5rem"})
        ])