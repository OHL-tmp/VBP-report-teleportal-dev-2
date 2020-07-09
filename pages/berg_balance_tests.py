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



#app = dash.Dash(__name__, url_base_pathname="/patient/")

#server = app.server


form={
'1':['1. SITTING TO STANDING',
['able to stand without using hands and stabilize independently',
'able to stand independently using hands',
'able to stand using hands after several tries',
'needs minimal aid to stand or to stabilize',
'needs moderate or maximal assist to stand',
],
[4,3,2,1,0],],
'2':['2. STANDING UNSUPPORTED',
['able to stand safely 2 minutes',
'able to stand 2 minutes with supervision',
'able to stand 30 seconds unsupported',
'needs several tries to stand 30 seconds unsupported',
'unable to stand 30 seconds unassisted',
],
[4,3,2,1,0],],
'3':['3. SITTING WITH BACK UNSUPPORTED BUT FEET SUPPORTED ON FLOOR OR ON A STOOL',
['able to sit safely and securely 2 minutes',
'able to sit 2 minutes under supervision',
'able to sit 30 seconds',
'able to sit 10 seconds',
'unable to sit without support 10 seconds',
],
[4,3,2,1,0],],
'4':['4. STANDING TO SITTING',
['sits safely with minimal use of hands',
'controls descent by using hands',
'uses back of legs against chair to control descent', 
'sits independently but has uncontrolled descent',
'needs assistance to sit',
],
[4,3,2,1,0],],
'5':['5. TRANSFERS',
['able to transfer safely with minor use of hands',
'able to transfer safely definite need of hands',
'able to transfer with verbal cueing and/or supervision',
'needs one person to assist',
'needs two people to assist or supervise to be safe',
],
[4,3,2,1,0],],
'6':['6. STANDING UNSUPPORTED WITH EYES CLOSED',
['able to stand 10 seconds safely',
'able to stand 10 seconds with supervision',
'able to stand 3 seconds',
'unable to keep eyes closed 3 seconds but stays steady',
'needs help to keep from falling',
],
[4,3,2,1,0],],
'7':['7. STANDING UNSUPPORTED WITH FEET TOGETHER',
['able to place feet together independently and stand 1 minute safely',
'able to place feet together independently and stand for 1 minute with supervision',
'able to place feet together independently but unable to hold for 30 seconds',
'needs help to attain position but able to stand 15 seconds with feet together',
'needs help to attain position and unable to hold for 15 seconds',
],
[4,3,2,1,0],],
'8':['8. REACHING FORWARD WITH OUTSTRETCHED ARM WHILE STANDING',
['can reach forward confidently >25 cm (10 inches)',
'can reach forward >12 cm safely (5 inches)',
'can reach forward >5 cm safely (2 inches)',
'reaches forward but needs supervision',
'loses balance while trying/requires external support',
],
[4,3,2,1,0],],
'9':['9. PICK UP OBJECT FROM THE FLOOR FROM A STANDING POSITION',
['able to pick up slipper safely and easily',
'able to pick up slipper but needs supervision',
'unable to pick up but reaches 2-5cm (1-2 inches) from slipper and keeps balance independently',
'unable to pick up and needs supervision while trying',
'unable to try/needs assist to keep from losing balance or falling',
],
[4,3,2,1,0],],
'10':['10. TURNING TO LOOK BEHIND OVER LEFT AND RIGHT SHOULDERS WHILE STANDING',
['looks behind from both sides and weight shifts well',
'looks behind one side only other side shows less weight shift',
'turns sideways only but maintains balance',
'needs supervision when turning',
'needs assist to keep from losing balance or falling',
],
[4,3,2,1,0],],
'11':['11. TURN 360 DEGREES',
['able to turn 360 degrees safely in 4 seconds or less',
'able to turn 360 degrees safely one side only in 4 seconds or less',
'able to turn 360 degrees safely but slowly',
'needs close supervision or verbal cueing',
'needs assistance while turning',
],
[4,3,2,1,0],],
'12':['12. PLACING ALTERNATE FOOT ON STEP OR STOOL WHILE STANDING UNSUPPORTED',
['able to stand independently and safely and complete 8 steps in 20 seconds',
'able to stand independently and complete 8 steps in >20 seconds',
'able to complete 4 steps without aid with supervision',
'able to complete >2 steps needs minimal assist',
'needs assistance to keep from falling/unable to try',
],
[4,3,2,1,0],],
'13':['13. STANDING UNSUPPORTED ONE FOOT IN FRONT',
['able to place foot tandem independently and hold 30 seconds',
'able to place foot ahead of other independently and hold 30 seconds',
'able to take small step independently and hold 30 seconds',
'needs help to step but can hold 15 seconds',
'loses balance while stepping or standing',
],
[4,3,2,1,0],],
'14':['14. STANDING ON ONE LEG',
['able to lift leg independently and hold >10 seconds',
'able to lift leg independently and hold 5-10 seconds',
'able to lift leg independently and hold = or >3 seconds',
'tries to lift leg unable to hold 3 seconds but remains standing independently',
'unable to try or needs assist to prevent fall',
],
[4,3,2,1,0],],
}

def berg_scale_button_template(label):
    return html.Div(
                [
                    html.Div(
                        dbc.Button( label, color="light",style={"border-radius":"10rem","width":"8rem"}, id = {'type':'berg-scale-question','index':label})
                    )
                ],
                style={"padding-bottom":"0.5rem"}   
            )

def physician_assess_group(label, value_list, value, id):
    value_list_len = len(value_list)

    options = []
    for i in range(value_list_len):
        options.append({"label":value_list[i], "value":value[i]})

    return html.Div(
            [
                dbc.FormGroup(
                    [
                        dbc.Label(label),
                        dbc.RadioItems(
                            options=options,
                            id = {'type':'berg-scale-question-content','index':id},
                            labelStyle={'display': 'block'},
                            style = {"textAlign" : "start"} ,
                        ),
                    ]
                )
            ],
            id={'type':'container-berg-scale-question-content','index':id},
            hidden=True,
        )

def modal_berg_scale_body():
	
	return html.Div(
            [
#                 dbc.Row(
#                     [
# #                        dbc.Col(width = 2),
#                         dbc.Col(berg_scale_button_template('1')),
#                         dbc.Col(berg_scale_button_template('2')),
#                         dbc.Col(berg_scale_button_template('3')),
#                         dbc.Col(berg_scale_button_template('4')),
#                         dbc.Col(berg_scale_button_template('5')),
#                         dbc.Col(berg_scale_button_template('6')),
#                         dbc.Col(berg_scale_button_template('7')),
#                     ],
#                     style = {"display" : "flex", "justify-content" : "space-around", "text-align" : "center"} 
#                 ),
#                 dbc.Row(
#                     [
# #                        dbc.Col(width = 2),
#                         dbc.Col(berg_scale_button_template('8')),
#                         dbc.Col(berg_scale_button_template('9')),
#                         dbc.Col(berg_scale_button_template('10')),
#                         dbc.Col(berg_scale_button_template('11')),
#                         dbc.Col(berg_scale_button_template('12')),
#                         dbc.Col(berg_scale_button_template('13')),
#                         dbc.Col(berg_scale_button_template('14')),
#                     ],
#                     style = {"display" : "flex", "justify-content" : "space-around", "text-align" : "center"} 
#                 ),
                html.Div(
                    html.Div(
                        [
                            berg_scale_button_template(str(i+1)) for i in range(14)
                        ],
                        style={"padding":"1rem"}
                    ),
                    style={"border-radius":"1rem", "background":"#f5f5f5", "padding":"0.5rem","width":"11rem","height":"20rem","overflow-y":"scroll"}
                ),
                html.Div(
                    [
                        dbc.Row(
                            [
        #                        dbc.Row(width = 2),
                                dbc.Col(html.Div( id = 'berg-scale-score')),
                            ],
                            style = {"display" : "flex", "justify-content" : "space-around", "text-align" : "center","padding-bottom":"2rem"} 
                        ),
                        dcc.Loading(
                            dbc.Row(
                                [
            #                        dbc.Row(width = 2),
                                    physician_assess_group(form['1'][0], form['1'][1], form['1'][2], '1'),
                                    physician_assess_group(form['2'][0], form['2'][1], form['2'][2], '2'),
                                    physician_assess_group(form['3'][0], form['3'][1], form['3'][2], '3'),
                                    physician_assess_group(form['4'][0], form['4'][1], form['4'][2], '4'),
                                    physician_assess_group(form['5'][0], form['5'][1], form['5'][2], '5'),
                                    physician_assess_group(form['6'][0], form['6'][1], form['6'][2], '6'),
                                    physician_assess_group(form['7'][0], form['7'][1], form['7'][2], '7'),
                                    physician_assess_group(form['8'][0], form['8'][1], form['8'][2], '8'),
                                    physician_assess_group(form['9'][0], form['9'][1], form['9'][2], '9'),
                                    physician_assess_group(form['10'][0], form['10'][1], form['10'][2], '10'),
                                    physician_assess_group(form['11'][0], form['11'][1], form['11'][2], '11'),
                                    physician_assess_group(form['12'][0], form['12'][1], form['12'][2], '12'),
                                    physician_assess_group(form['13'][0], form['13'][1], form['13'][2], '13'),
                                    physician_assess_group(form['14'][0], form['14'][1], form['14'][2], '14'),

                                ],
                                style = {"display" : "flex", "justify-content" : "space-around", "text-align" : "center"} 
                            )
                        ),
                        dbc.Row(
                            [
        #                        dbc.Row(width = 2),
                                dbc.Col(
                                    html.Div(
                                        [
                                            dbc.Button('Next', color="dark",style={"border-radius":"10rem"}, id = 'berg-scale-question-next')
                                        ]
                                    )
                                ),
                            ],
                            style = {"display" : "flex", "justify-content" : "space-around", "text-align" : "center"}
                        ),
                    ],
                    style={"width":"30rem","padding-left":"4rem"}
                ),
        ],
        style={"display":"flex"}
    )


#app.layout = modal_berg_scale_body()

# @app.callback(
#     [Output(f'container-berg-scale-question-content-{i+1}', "hidden") for i in range(14)]
#     +[Output("berg-scale-question-next", "disabled")],
#     [Input(f'berg-scale-question-{i+1}', "n_clicks") for i in range(14)]
#     +[Input("berg-scale-question-next", "n_clicks"),],
#     [State(f'container-berg-scale-question-content-{i+1}', "hidden") for i in range(14)
#     ],
#     )
# def switch_questions(q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14, next,qc1,qc2,qc3,qc4,qc5,qc6,qc7,qc8,qc9,qc10,qc11,qc12,qc13,qc14):
#     disable=False
#     ctx = dash.callback_context
#     if ctx.triggered[0]['prop_id'].split('.')[0] == 'berg-scale-question-next':

#         qc=[qc1,qc2,qc3,qc4,qc5,qc6,qc7,qc8,qc9,qc10,qc11,qc12,qc13,qc14]
#         selected_index=[j for j, e in enumerate(qc) if e == False]
#         num=selected_index[0]
#         if num==12:
#             disable=True
#             qc[12]=True
#             qc[13]=False
#         elif num==13:
#             disable=True
#             qc[13]=False
#         else: 
#             disable=False
#             qc[num]=True
#             qc[num+1]=False

#     else:
#         qc=[True]*14
#         triggered_button=ctx.triggered[0]['prop_id'].split('.')[0]
#         if triggered_button=='':
#             qc[0]=False
#         else:
#             num=int(triggered_button[20:])            
#             qc[num-1]=False
#             if num==14:
#                 disable=True
#             else:
#                 disable=False

    
#     return qc[0], qc[1], qc[2],qc[3],qc[4],qc[5],qc[6],qc[7],qc[8],qc[9],qc[10], qc[11], qc[12],qc[13],disable

# @app.callback(
#     [Output("berg-scale-score", "children"),
#     Output({"type": "physician-assessment-collapse-score", 'index':'0-0'},"children")],
#     [Input(f'berg-scale-question-content-{i+1}', "value") for i in range(14)]
#     )
# def cal_score(q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14):
#     pl = list(filter(None, [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14]))
#     if len(pl)==0:
#         score=0
#     else:
#         score=sum(pl)
#     return 'Total Score: '+str(score)+'/56', str(score)



if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True,port=8049)