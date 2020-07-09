import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import time

import base64
import cv2
import datetime
import json
import pandas as pd
import numpy as np
import glob
import os

from dash.dependencies import Input, Output, State
from statistics import mean

# from utils import *
# from app import app
from kccq_questionnaire_answer_prior2 import *
from berg_balance_tests import *
from figure import *

def patient_data(data, pid):
    data_filtered = [item for item in data if item[5] == pid]
    data_dict = dict(patient_data=data_filtered)

    return html.Div(children = json.dumps(data_dict), style = {'display':'none'}, id = {"type": "physician-patient-store-detail", 'index': pid})

def patient_item(app, name, dob, age, gender, current_assessment, assessments_2breviewed, review_duedate, icon, pid):
    return html.Div(
            [
                dbc.Button(
                    html.Div(
                        [
                            html.Div(
                                html.Img(src=app.get_asset_url("profile_default"+str(icon)+".png"), style={"height":"2.5rem", "padding-top":"0px"}),
                                style={"width":"4rem"}
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Div(
                                            html.H1(name, style={"font-size":"1rem"}),
                                            style={"text-align":"start","padding-left":"0.5rem"}
                                        ),
                                        width=2
                                    ),
                                    dbc.Col(
                                        html.Div(
                                            html.H6(dob, style={"font-size":"1rem"})
                                        ),
                                        width=2
                                    ),
                                    dbc.Col(
                                        html.Div(
                                            html.H6(str(age), style={"font-size":"1rem"})
                                        ),
                                        width=1
                                    ),
                                    dbc.Col(
                                        html.Div(
                                            html.H6(gender, style={"font-size":"1rem"})
                                        ),
                                        width=1
                                    ),
                                    dbc.Col(
                                        html.Div(
                                            html.H6(str(current_assessment), style={"font-size":"1rem"})
                                        ),
                                        width=2
                                    ),
                                    dbc.Col(
                                        html.Div(
                                            [
                                                html.H1(str(assessments_2breviewed), style={"font-size":"1rem","color":"#fff","background-color":"#dc3545","border-radius":"10rem","width":"1.6rem","padding":"0.2rem","margin-left":"3rem","margin-top":"-0.2rem"}, id={"type": "physician-patient-assessments_2breviewed", 'index': pid})
                                            if assessments_2breviewed > 0
                                            else
                                                html.H1("--", style={"font-size":"1rem","color":"#000","background-color":"#fff","border-radius":"10rem","width":"1.6rem","padding":"0.2rem","margin-left":"3rem","margin-top":"-0.2rem"}, id={"type": "physician-patient-assessments_2breviewed", 'index': pid}),
                                            ],
                                            style={"text-align":"center"}
                                        ),
                                        width=2
                                    ),
                                    dbc.Col(
                                        html.Div(
                                            html.H6(review_duedate, style={"font-size":"1rem"})
                                        ),
                                        width=2
                                    ),
                                ],
                                style={"width":"100%","margin-top":"0.5rem"}
                            )
                        ],
                        style={"display":"flex"}
                    ),
                    color="light",
                    outline=True,
                    id={"type": "physician-open-patient", 'index': pid},
                    style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)","padding-left":"1rem","padding-right":"2rem", "border-radius":"10rem","text-align":"center","padding-top":"1rem","padding-bottom":"1rem","width":"100%"}
                ),
                dbc.Modal(
                        [
                            
                            dbc.ModalBody(
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.Img(src=app.get_asset_url("profile_default"+str(icon)+".png"), style={"height":"80px", "padding":"10px","margin-top":"30px"}),
                                                        html.Div(
                                                            [
                                                                html.H2(name, style={"font-size":"1.6rem", "color":"#000", "padding-bottom":"32px", "padding-top":"16px"}),
                                                                html.H6("DATE OF BIRTH", style={"font-size":"0.6rem"}),
                                                                html.Div(dbc.Badge(str(dob), pill=True, style={"background":"#857698"}), style={"margin-top":"-10px", "padding-bottom":"16px"}),
                                                                html.H6("AGE", style={"font-size":"0.6rem"}),
                                                                html.Div(dbc.Badge(str(age), pill=True, style={"background":"#857698"}), style={"margin-top":"-10px", "padding-bottom":"16px"}),
                                                                html.H6("GENDER", style={"font-size":"0.6rem"}),
                                                                html.Div(dbc.Badge(str(gender), pill=True, style={"background":"#857698"}), style={"margin-top":"-10px", "padding-bottom":"16px"}),
                                                            ]
                                                        )
                                                    ],
                                                    style={"padding":"20px","text-align":"center"}
                                                ),
                                            ],
                                            style={"width":"260px", "border-radius":"1rem","background":"#f5f5f5","margin-top":"60px","margin-left":"20px"}
                                        ),
                                        html.Div(
                                            [
                                            html.Div([
                                                html.H6("Sort By"),
                                                dbc.Select(
                                                id = {'type':'physician-modal-select-sorting', 'index':pid},
                                                options = [
                                                    {"label":"Category", "value":0},
                                                    {"label":"Patient Completion Date", "value":3},
                                                ],
                                                value = 0,
                                                bs_size = 'sm',
                                                )]),
                                            html.Div([],id = {'type':'physician-modal-patient-modalbody', 'index':pid}),    
                                            ],
                                            style={"padding-left":"20px","margin-top":"60px"}
                                        ),
                                    ],
                                    style={"display":"flex", "padding-bottom":"60px"}
                                )
                            ),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "CLOSE", id={"type": "physician-close-patient", 'index': pid}, className="ml-auto",
                                    style={"margin-right":"20px", "background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Black", "font-size":"1rem"}
                                )
                            ),
                        ],
                        id={"type": "physician-modal-patient", 'index': pid},
                        size='xl',
                        scrollable=False,
                        backdrop = 'static',
                    ),
            ],
            style={"padding-left":"5rem","padding-right":"7rem","padding-top":"0.5rem"}
        )


def physician_assessment_item(category,assessment,assessment_type,Completion_date, result, pid, itemid):
    cd = datetime.datetime.strptime(Completion_date, '%m/%d/%Y')
    rd = cd + datetime.timedelta(days = 7)
    rd = str(datetime.datetime.strftime(rd, '%m/%d/%Y'))
    if rd > str(datetime.datetime.now().date()):
        color = "#dc3545"
    else:
        color = "#000"
    return html.Div(
            [
                html.Div([
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H1(assessment, style={"font-size":"1.5rem"}),
                                    html.Div(
                                        [

                                            dbc.Badge(category, color="info", style={"font-family":"NotoSans-Light","font-size":"0.8rem"}),
                                            html.H6("Dr.Smith", style={"padding-left":"0.5rem","padding-right":"0.5rem"}),
                                            html.H6(" | "),
                                            html.H6(assessment_type, style={"padding-left":"0.5rem","padding-right":"0.5rem"}),
                                        ],
                                        style={"display":"flex","font-size":"0.8rem"}
                                    ),
                                ],
                                style={"width":"26rem","padding-left":"10px"}
                            ),
                            html.Div(
                                [
                                    html.H6("Patient Completion Date", style={"font-size":"0.6rem","height":"1.5rem"}),
                                    html.H1(Completion_date, style={"font-size":"1.2rem","text-align":"center"}, 
#                                        id = u'patient-assessment-completdate-{}'.format(num)
                                        )
                                ],
                                style={"border-left":"1px solid #d0d0d0","padding-left":"1rem","padding-right":"1rem"}
                            ),
                            html.Div(
                                [
                                    html.H6("Review Due Date", style={"font-size":"0.6rem","height":"1.5rem"}),
                                    html.H1(rd, style={"font-size":"1.2rem","color":color}, 
#                                        id = u'patient-assessment-status-{}'.format(num)
                                        )
                                ],
                                style={"border-left":"1px solid #d0d0d0","padding-left":"1rem","padding-right":"1rem"}, 
                            ),
                            html.Div(
                                [  
                                    dcc.Loading(
                                        dbc.Button(result, id = {"type": "physician-assessment-open-item", 'index': str(pid)+'-'+str(itemid)}, style={"border-radius":"10rem"}, color="warning")
                                    ),
                                ],
                                style={"border-left":"1px solid #d0d0d0","padding-left":"1rem","padding-right":"1rem","width":"6rem"}
                            ),
                        ],
                        style={"display":"flex","padding-top":"1rem","padding-bottom":"1rem","justify-content":"space-around"}
                    ),
                    html.Div([
                        dbc.Collapse(patient_collapse_item(assessment_type, Completion_date, result, pid, itemid), id = {"type": "physician-assessment-collapse", 'index': str(pid)+'-'+str(itemid)})
                        ]
                    ),],
                    style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)","padding-left":"0.5rem","padding-right":"1rem", "border-radius":"0.8rem"}
                )
            ],
            style={"padding":"0.5rem"}
        )

def patient_collapse_item(assessment_type, Completion_date, result, pid, itemid):

    cd = datetime.datetime.strptime(Completion_date, '%m/%d/%Y')
    submit_date = str(cd.date())
    if assessment_type == "Self Recording":
        path = str('../configure/demo-patient/upload/') + submit_date + str('_')
        file = glob.glob(path +'*.*')[0].replace('\\','/')
        encoded_video = base64.b64encode(open(file, 'rb').read())
        review_video = html.Div(
                            [
                                html.Video(src='data:image/png;base64,{}'.format(encoded_video.decode()), controls = True, style={"height":"16rem","border-bottom":"none", "text-align":"center"} ),
                            ]
                        )
        cap = cv2.VideoCapture(file)
        if cap.isOpened(): 
            rate = cap.get(5)   
            FrameNumber = cap.get(7) 
            duration = int(FrameNumber/rate)

        size = round(os.path.getsize(file)/(1024*1024),1)
        
        if result == "Start Review":
            score_div = html.Div(
                            [
                                html.H2("Physician Assessment", style={"font-size":"0.8rem"}),
                                modal_berg_scale_body(),
                                html.Div(style = {'display':'none'}, id= {"type": "physician-assessment-collapse-score", 'index': str(pid)+'-'+str(itemid)})
                            ]
                        )
        else:
            score_div = [html.Div(id= {"type": "physician-assessment-collapse-score", 'index': str(pid)+'-'+str(itemid)})]
        
        return html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(review_video),
                                dbc.Col(
                                    [
                                        dbc.Row("Video Uploaded on:  " + Completion_date),
                                        dbc.Row("Video Length:  " + str(duration) + 's'),
                                        dbc.Row("Video Size:  " + str(size) + 'MB')
                                    ],
                                    style={"font-size":"0.8rem"}
                                )
                            ],
                            style={"padding":"16px"}
                        ),
                        html.Hr(),
                        dbc.Row(
                            [
                                html.Div(
                                    [
                                        
                                        html.Div(score_div),
                                    ]
                                )
                            ]
                        ),
                        
                        html.Div(
                            dbc.Button("Finish", id= {"type": "physician-assessment-collapse-close", 'index': str(pid)+'-'+str(itemid)}),
                            style={"text-align":"end","padding":"1rem"}
                        ),
                        
                    ],
                    style={"padding-left":"2rem"}
                )
    else:
        file = str('../configure/demo-patient/kccq_questionarie_' + submit_date + '.json')
        answer = json.load(open(file), encoding = 'utf-8')
        pl_score, sf_score, ql_score, sl_score, all_score = cal_kccq_score(answer)
        current_score = [pl_score, sf_score, ql_score, sl_score, all_score]
        df=data_process(df_kccq_score,current_score,Completion_date)
        if result == "Start Review":
            summary_graph = [
                html.Div(all_score, style = {'display':'none'}, id= {"type": "physician-assessment-collapse-score", 'index': str(pid)+'-'+str(itemid)}),
                html.Div(children=tbl(df),style={"padding":"2rem"}),
                dcc.Graph(figure=bargraph(df),config={'displayModeBar': False},style={"padding":"2rem"}),]
        else: 
            summary_graph = [html.Div(id= {"type": "physician-assessment-collapse-score", 'index': str(pid)+'-'+str(itemid)})]
        return html.Div([
            html.H2("KCCQ_12 Questionnaire submitted by " + Completion_date, style={"font-size":"0.8rem"}),
            html.Hr(),
            dbc.Row([
                dbc.Col("Physical Limitation"),
                dbc.Col("Symptom Frequency"),
                dbc.Col("Quality of Life"),
                dbc.Col("Social Limitation"),
                dbc.Col("Summary Score"),
                ],style={"padding-left":"1rem","padding-right":"1rem"}),
            dbc.Row([
                dbc.Col(pl_score,style={"text-align":"text"}),
                dbc.Col(sf_score,style={"text-align":"text"}),
                dbc.Col(ql_score,style={"text-align":"text"}),
                dbc.Col(sl_score,style={"text-align":"text"}),
                dbc.Col(all_score,style={"text-align":"text"}),
                ],style={"text-align":"text","padding-left":"1rem","padding-right":"1rem"}),
            html.Hr(),
            html.Div(summary_graph, id= {"type": "physician-assessment-graph-kccq-summary", 'index': str(pid)+'-'+str(itemid)}),
            html.Div(
                html.Div(
                    modal_kccq_questionaire_body_answer_prior(answer),
                ),
                style={"overflow-y":"scroll","height":"80vh","border":"1px solid #000"}
            ),
            html.Div(
                dbc.Button("Finish", id= {"type": "physician-assessment-collapse-close", 'index': str(pid)+'-'+str(itemid)}),style={"text-align":"end","padding":"1rem"}
            ),
            ],style={"padding":"1rem", "width":"100%"})

def cal_kccq_score(answer):
    pl = list(filter(None, [answer['q1a'],answer['q1b'],answer['q1c']]))
    sf = list(filter(None, [answer['q2'],answer['q3'],answer['q4'],answer['q5']]))
    ql = list(filter(None, [answer['q6'],answer['q7']]))
    sl = list(filter(None, [answer['q8a'],answer['q8b'],answer['q8c']]))

    pl_score = round(mean(pl),0) if len(pl) > 0 else 0
    sf_score = round(mean(sf),0) if len(sf) > 0 else 0
    ql_score = round(mean(ql),0) if len(ql) > 0 else 0
    sl_score = round(mean(sl),0) if len(sl) > 0 else 0

    allanswer = pl + sf + ql + sl
    summary_score = round(mean(allanswer),0) if len(allanswer) > 0 else 0
    return pl_score, sf_score, ql_score, sl_score, summary_score


if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True,port=8052)