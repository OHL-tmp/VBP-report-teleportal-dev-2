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


from flask_login import logout_user, current_user

from dash.dependencies import Input, Output, State
from server import app, server



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

def modal_kccq_questionaire_answer_prior(app, filename, num):
    path = 'configure/' + current_user.email + '/' + filename
    answer = json.load(open(path, encoding = 'utf-8'))
    return html.Div(
            [
                html.H6("Review", style={"font-size":"0.7rem","padding-top":"10px"}),
                dbc.Button(children = [html.Img(src=app.get_asset_url("icon-inspection-100.png"), style={"height":"1.5rem", "padding-top":"0px"})], color="light",style={"border-radius":"10rem"}, id = u'kccq-modal-answer-prior-button-open-{}'.format(num)),
                dbc.Modal(
                    [
                        dbc.ModalHeader(
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H1("KCCQ Questionnaire", style={"font-size":"1.6rem","padding-right":"30px"}),
                                            dbc.Badge(answer["answer-date"] + " Completed", color="primary", className="mr-1",style={"font-family":"NotoSans-SemiBold","font-size":"1rem"}),
                                        ]
                                    ),
                                    html.H6("Instructions: The following questions refer to your heart failure and how it may affect your life. Please read and complete the following questions. There are no right or wrong answers. Please mark the answer that best applies to you.")
                                ],
                                style={"width":"80%","padding-left":"40px","padding-right":"40px","padding-top":"10px","padding-bottom":"10px"}
                            )
                        ),
                        dbc.ModalBody(
                            modal_kccq_questionaire_body_answer_prior(answer, num),
                            style={"padding":"40px","margin-top":"-20px"}
                        ),
                        dbc.ModalFooter(
                            dbc.Button("Close", id=u"kccq-modal-answer-prior-button-submit-{}".format(num), className="mr-2"),
                        )
                    ],
                    id = u"kccq-modal-answer-prior-{}".format(num),
                    size = 'xl',
                    backdrop = "static"
                )
            ]
        )

def modal_kccq_questionaire_body_answer_prior( answer, num=1):
	
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
                                                dbc.Col(width = 2),
                                                dbc.Col("Extremely Limited"),
                                                dbc.Col("Quite a bit Limited"),
                                                dbc.Col("Moderately Limited"),
                                                dbc.Col("Slightly Limited"),
                                                dbc.Col("Not at all Limited"),
                                                dbc.Col("Limited for other reasons or did not do the activity"),
                                            ],
                                            style = {"display" : "flex", "justify-content" : "space-around", "text-align" : "center"} 
                                        )
                                    ),
                                    html.Hr(),
                                    html.Div(
                                        dbc.Row(
                                            [
                                                dbc.Col("a. Showering/bathing", width = 2),
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
                                                        value = answer['q1a'],
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
                                                dbc.Col("b. Walking 1 block on level ground",width = 2),
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
                                                        value = answer['q1b'],
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
                                                dbc.Col("c. Hurrying or jogging (as if to catch a bus)",width = 2),
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
                                                        value = answer['q1c'],
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
                    question_group_answer_prior(q2[0], q2[1], q2[2], "q2", answer),
                    question_group_answer_prior(q3[0], q3[1], q3[2], "q3", answer),
                    question_group_answer_prior(q4[0], q4[1], q4[2], "q4", answer),
                    question_group_answer_prior(q5[0], q5[1], q5[2], "q5", answer),
                    question_group_answer_prior(q6[0], q6[1], q6[2], "q6", answer),
                    question_group_answer_prior(q7[0], q7[1], q7[2], "q7", answer),
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
                                                dbc.Col(width = 2),
                                                dbc.Col("Severely Limited"),
                                                dbc.Col("Limited quite a bit"),
                                                dbc.Col("Moderately Limited"),
                                                dbc.Col("Slightly Limited"),
                                                dbc.Col("Did not limit at all"),
                                                dbc.Col("Does not apply or did not do for other reasons"),
                                            ],
                                            style = {"display" : "flex", "justify-content" : "space-around", "text-align" : "center"} 
                                        )
                                    ),
                                    html.Hr(),
                                    html.Div(
                                        dbc.Row(
                                            [
                                                dbc.Col("a. Hobbies, recreational activities", width = 2),
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
                                                        value = answer['q8a'],
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
                                                dbc.Col("b. Working or doing household chores",width = 2),
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
                                                        value = answer['q8b'],
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
                                                dbc.Col("c. Visiting family or friends out of your home",width = 2),
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
                                                        value = answer['q8c'],
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


def question_group_answer_prior(label, value_list, value, key, answer):
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
                            value = answer[key],
                            style={"font-size":"0.8rem","padding":"20px","border-radius":"0.5rem","background":"#f5f5f5"}
                        ),
                    ],
                    style={"padding":"20px"}
                )
            ]
        )

