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
import os

from dash.dependencies import Input, Output, State
# from server import app, server



q2=["2. Over the past 2 weeks, how many times did you have swelling in your feet, ankles or legs when you woke up in the morning?",
["Every morning",
"3 or more times per week but not every day",
"1-2 times per week",
"Less than once a week",
"Never over the past 2 weeks"],
[20,40,60,80,100], 'SF']

q3=["3. Over the past 2 weeks, on average, how many times has fatigue limited your ability to do what you wanted?",
["All of  the time",
"Several times per day",
"At least once a day",
"3 or more times per week but not every day",
"1-2 times per week",
"Less than once a week",
"Never over the  past 2 weeks"],
[15,30,45,60,75,90,100], 'SF']

q4=["4. Over the past 2 weeks, on average, how many times has shortness of breath limited your ability to do what you wanted?",
["All of  the time",
"Several times per day",
"At least once a day",
"3 or more times per week but not every day",
"1-2 times per week",
"Less than once a week",
"Never over the  past 2 weeks"],
[15,30,45,60,75,90,100], 'SF']

q5=["5. Over the past 2 weeks, on average, how many times have you been forced to sleep sitting up in a chair or with at least 3 pillows to prop you up because of shortness of breath?",
["Every night",
"3 or more times per week but not every day",
"1-2 times per week",
"Less than once a week",
"Never over the  past 2 weeks"],
[30,40,60,80,100], "SF"]

q6=["6. Over the past 2 weeks, how much has your heart failure limited your enjoyment of life?",
["It has extremely  limited my enjoyment of life",
"It has limited my enjoyment of life quite a bit",
"It has moderately  limited my enjoyment of life",
"It has slightly  limited my enjoyment of life",
"It has not limited  my enjoyment of life at all",],
[20,40,60,80,100], "QL"]

q7=["7. If you had to spend the rest of your life with your heart failure the way it is right now, how would you feel about this?",
["Not at all satisfied",
"Mostly dissatisfied",
"Somewhat satisfied",
"Mostly satisfied",
"Completely satisfied",],
[20,40,60,80,100], "QL"]

def modal_kccq_questionaire_answer(app):
    return html.Div(
                [
                    html.H6("Review", style={"font-size":"0.7rem","padding-top":"10px"}),
                    dbc.Button(children = [html.Img(src=app.get_asset_url("icon-inspection-100.png"), style={"height":"1.5rem", "padding-top":"0px"})], color="light",style={"border-radius":"10rem"}, id = 'kccq-modal-answer-button-open'),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(id = "kccq-modal-answer-header"),
                            dbc.ModalBody(
                                modal_kccq_questionaire_body_answer(),
                                style={"padding":"40px","margin-top":"-20px"}
                            ),
                            dbc.ModalFooter(
                                dbc.Button("Close", id="kccq-modal-answer-button-submit", className="mr-2",style={"width":"160px"}),
                                style={"padding-right":"42%"}
                            )
                        ],
                        id = "kccq-modal-answer",
                        size = 'xl',
                        backdrop = "static"
                    )
                ],
                style={"text-align":"center"}
            )

def modal_kccq_questionaire_body_answer():
	
	return html.Div(
                [
                    
                    html.Div(
                        [
                            html.Div(
                                    "1. Heart failure affects different people in different ways. Some feel shortness of breath while others feel fatigue. Please indicate how much you are limited by heart failure (shortness of breath or fatigue) in your ability to do the following activities over the past 2 weeks.",
                                    style={"padding-top":"10px","padding-bottom":"10px"}
                                ),
                            html.Div(
                                [
                                    html.Div(
                                        dbc.Row(
                                            [
                                                dbc.Col(width = 3),
                                                dbc.Col("Extremely Limited"),
                                                dbc.Col("Quite a bit Limited"),
                                                dbc.Col("Moderately Limited"),
                                                dbc.Col("Slightly Limited"),
                                                dbc.Col("Not at all Limited"),
                                                dbc.Col("Limited for other reasons or did not do the activity"),
                                            ],
                                            style = {"display" : "flex", "justify-content" : "space-around", "text-align" : "center","font-family":"NotoSans-SemiBold"} 
                                        )
                                    ),
                                    html.Hr(),
                                    html.Div(
                                        dbc.Row(
                                            [
                                                dbc.Col("a. Showering/bathing", width = 3),
                                                dbc.Col(
                                                    dbc.RadioItems(
                                                        options = [
                                                            {"label": "", "value" : 20, "disabled" : True},
                                                            {"label": "", "value" : 40, "disabled" : True},
                                                            {"label": "", "value" : 60, "disabled" : True},
                                                            {"label": "", "value" : 80, "disabled" : True},
                                                            {"label": "", "value" : 100, "disabled" : True},
                                                            {"label": "", "value" : 50, "disabled" : True},
                                                            ],
                                                        id = "kccq-modal-answer-radio-q1a",
                                                        inline = True,
                                                        style = {"display" : "flex", "justify-content" : "space-around"} ),
                                                    
                                                    ),
                                            ]
                                        )
                                    ),
                                    html.Hr(),
                                    html.Div(
                                        dbc.Row(
                                            [
                                                dbc.Col("b. Walking 1 block on level ground",width = 3),
                                                dbc.Col(
                                                    dbc.RadioItems(
                                                        options = [
                                                            {"label": "", "value" : 20, "disabled" : True},
                                                            {"label": "", "value" : 40, "disabled" : True},
                                                            {"label": "", "value" : 60, "disabled" : True},
                                                            {"label": "", "value" : 80, "disabled" : True},
                                                            {"label": "", "value" : 100, "disabled" : True},
                                                            {"label": "", "value" : 50, "disabled" : True},
                                                            ],
                                                        id = "kccq-modal-answer-radio-q1b",
                                                        inline = True,
                                                        style = {"display" : "flex", "justify-content" : "space-around"} ),
                                                    
                                                    ),
                                            ]
                                        )
                                    ),
                                    html.Hr(),
                                    html.Div(
                                        dbc.Row(
                                            [
                                                dbc.Col("c. Hurrying or jogging (as if to catch a bus)",width = 3),
                                                dbc.Col(
                                                    dbc.RadioItems(
                                                        options = [
                                                            {"label": "", "value" : 20, "disabled" : True},
                                                            {"label": "", "value" : 40, "disabled" : True},
                                                            {"label": "", "value" : 60, "disabled" : True},
                                                            {"label": "", "value" : 80, "disabled" : True},
                                                            {"label": "", "value" : 100, "disabled" : True},
                                                            {"label": "", "value" : 50, "disabled" : True},
                                                            ],
                                                        id = "kccq-modal-answer-radio-q1c",
                                                        inline = True,
                                                        
                                                        style = {"display" : "flex", "justify-content" : "space-around"} ),
                                                    
                                                    ),
                                            ]
                                        )
                                    ),
                                ],
                                style={"font-size":"0.8rem","padding":"20px","border-radius":"0.5rem","background":"#f5f5f5"}
                            )
                        ],
                        style={"padding":"20px"}
                    ),
                    question_group_answer(q2[0], q2[1], q2[2], "kccq-modal-answer-radio-q2"),
                    question_group_answer(q3[0], q3[1], q3[2], "kccq-modal-answer-radio-q3"),
                    question_group_answer(q4[0], q4[1], q4[2], "kccq-modal-answer-radio-q4"),
                    question_group_answer(q5[0], q5[1], q5[2], "kccq-modal-answer-radio-q5"),
                    question_group_answer(q6[0], q6[1], q6[2], "kccq-modal-answer-radio-q6"),
                    question_group_answer(q7[0], q7[1], q7[2], "kccq-modal-answer-radio-q7"),
                    html.Div(
                        [
                            html.Div(
                                    "8. How much does your heart failure affect your lifestyle? Please indicate how your heart failure may have limited your participation in the following activities over the past 2 weeks.",
                                    style={"padding-top":"10px","padding-bottom":"10px"}
                                ),
                            html.Div(
                                [
                                    html.Div(
                                        dbc.Row(
                                            [
                                                dbc.Col(width = 3),
                                                dbc.Col("Severely Limited"),
                                                dbc.Col("Limited quite a bit"),
                                                dbc.Col("Moderately Limited"),
                                                dbc.Col("Slightly Limited"),
                                                dbc.Col("Did not limit at all"),
                                                dbc.Col("Does not apply or did not do for other reasons"),
                                            ],
                                            style = {"display" : "flex", "justify-content" : "space-around", "text-align" : "center","font-family":"NotoSans-SemiBold"} 
                                        )
                                    ),
                                    html.Hr(),
                                    html.Div(
                                        dbc.Row(
                                            [
                                                dbc.Col("a. Hobbies, recreational activities", width = 3),
                                                dbc.Col(
                                                    dbc.RadioItems(
                                                        options = [
                                                            {"label": "", "value" : 20, "disabled" : True},
                                                            {"label": "", "value" : 40, "disabled" : True},
                                                            {"label": "", "value" : 60, "disabled" : True},
                                                            {"label": "", "value" : 80, "disabled" : True},
                                                            {"label": "", "value" : 100, "disabled" : True},
                                                            {"label": "", "value" : 70, "disabled" : True},
                                                            ],
                                                        id = "kccq-modal-answer-radio-q8a",
                                                        inline = True,
                                                        style = {"display" : "flex", "justify-content" : "space-around"} ),
                                                    
                                                    ),
                                            ]
                                        )
                                    ),
                                    html.Hr(),
                                    html.Div(
                                        dbc.Row(
                                            [
                                                dbc.Col("b. Working or doing household chores",width = 3),
                                                dbc.Col(
                                                    dbc.RadioItems(
                                                        options = [
                                                            {"label": "", "value" : 20, "disabled" : True},
                                                            {"label": "", "value" : 40, "disabled" : True},
                                                            {"label": "", "value" : 60, "disabled" : True},
                                                            {"label": "", "value" : 80, "disabled" : True},
                                                            {"label": "", "value" : 100, "disabled" : True},
                                                            {"label": "", "value" : 70, "disabled" : True},
                                                            ],
                                                        id = "kccq-modal-answer-radio-q8b",
                                                        inline = True,
                                                        style = {"display" : "flex", "justify-content" : "space-around"} ),
                                                    
                                                    ),
                                            ]
                                        )
                                    ),
                                    html.Hr(),
                                    html.Div(
                                        dbc.Row(
                                            [
                                                dbc.Col("c. Visiting family or friends out of your home",width = 3),
                                                dbc.Col(
                                                    dbc.RadioItems(
                                                        options = [
                                                            {"label": "", "value" : 20, "disabled" : True},
                                                            {"label": "", "value" : 40, "disabled" : True},
                                                            {"label": "", "value" : 60, "disabled" : True},
                                                            {"label": "", "value" : 80, "disabled" : True},
                                                            {"label": "", "value" : 100, "disabled" : True},
                                                            {"label": "", "value" : 70, "disabled" : True},
                                                            ],
                                                        id = "kccq-modal-answer-radio-q8c",
                                                        inline = True,
                                                        
                                                        style = {"display" : "flex", "justify-content" : "space-around"} ),
                                                    
                                                    ),
                                            ]
                                        )
                                    ),
                                ],
                                style={"font-size":"0.8rem","padding":"20px","border-radius":"0.5rem","background":"#f5f5f5"}
                            )
                        ],
                        style={"padding":"20px"}
                    ),
                ],
                # style={"margin-top":"-30rem","background-color":"transparent","text-align":"center"}
            )


def question_group_answer(label, value_list, value, id):
    value_list_len = len(value_list)

    options = []
    for i in range(value_list_len):
        options.append({"label":value_list[i], "value":value[i], "disabled" : True})

    return html.Div(
            [
                dbc.FormGroup(
                    [
                        dbc.Label(label,style={"padding-top":"10px","padding-bottom":"10px"}),
                        dbc.RadioItems(
                            options=options,
                            id=id,
                            style={"font-size":"0.8rem","padding":"20px","border-radius":"0.5rem","background":"#f5f5f5"}
                        ),
                    ],
                    style={"padding":"20px"}
                )
            ]
        )


