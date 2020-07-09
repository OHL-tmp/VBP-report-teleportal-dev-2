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

from dash.dependencies import Input, Output, State, MATCH, ALL

# from utils import *
# from app import app

# from kccq_questionnaire2 import *
from kccq_questionnaire_answer2 import *

from patient_page import *



app = dash.Dash(__name__, url_base_pathname='/physician/')
server = app.server
app.config['suppress_callback_exceptions'] = True

username = "demo-physician"
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
								html.H2("Physician Login",style={"font-size":"1.6rem","padding-left":"20px"}),
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
											[
												html.Form(
													[
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
													action='/login', 
													method='post'
												)
											]
										)
									],
									style={"padding-left":"2rem","padding-right":"2rem"}
								),
								className="mb-3",
								style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.1), 0 6px 20px 0 rgba(0, 0, 0, 0.1)", "border":"none", "border-radius":"1rem"}
							)
						],
						style={"background-color":"transparent", "border":"none", "width":"500px", "margin":"auto", "padding-top":"5vh"}
					),
				],
				style={"background":"url(./assets/physician-login.png)","height":"100vh"},
				id="login-layout"
			)


def physician_layout(app):
	return html.Div(
				[
					header(app),
					html.Div(style={"height":"0rem"}),
					html.Div(
						[
							card_mainlist(app)
						],
						style={"padding-top":"1rem","background-color":"#fff"}
					),
				],
				id="physician-layout"
			)



def header(app):
	search_bar = dbc.Row(
		[
			dbc.Col(
				dbc.Button(
					"Log Out", 
					outline=True, 
					color="dark", 
					style={"border-radius":"10rem", "width":"6rem","height":"2rem","font-size":"0.7rem"},
					id = "logout-button"
				),
				width="auto",
			),
		],
		no_gutters=True,
		className="ml-auto flex-nowrap mt-3 mt-md-0",
		align="center",
	)

	header = dbc.Navbar(
			[
				html.A(
					# Use row and col to control vertical alignment of logo / brand
					dbc.Row(
						[
							dbc.Col(html.Img(src=app.get_asset_url("profile_default4.png"), style={"height":"2.5rem", "padding-top":"0px"}), style={"padding-right":"2rem"}, width="auto"),
							dbc.Col(
								html.Div(
									[
										html.H1("Dr. Richard Smith", style={"font-size":"1rem", "line-height":"0.6"}),
										html.H6("NPI : 0000000001", style={"font-size":"0.8rem"}),
									],
									style={"padding-top":"0.5rem"}
								), width="auto"),
							dbc.Col(width=3),
							dbc.Col(
								html.Div(
									[
										html.H1("Area of Specialty", style={"font-size":"0.8rem", "line-height":"0.6"}),
										html.H6("Cardiology", style={"font-size":"0.8rem"}),
									],
									style={"padding-top":"0.5rem"}
								), width="auto"),
							dbc.Col(width=1),
							dbc.Col(
								html.Div(
									[
										html.H1("Organization", style={"font-size":"0.8rem", "line-height":"0.6"}),
										html.H6("Demo Cardiology Physician Group", style={"font-size":"0.8rem"}),
									],
									style={"padding-top":"0.5rem"}
								), width="auto"),
						],
						align="center",
						no_gutters=True,
						style={"width":"50rem"}
					),
				),
				dbc.NavbarToggler(id="navbar-toggler"),
				dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
			],
			color="#fff",
			sticky = "top",
			expand = True,
			className="sticky-top",
			style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)","padding-left":"8rem","padding-right":"8rem","padding-top":"1rem","padding-bottom":"1rem"}
#            dark=True,
		)
	return header
	

def card_mainlist(app):

	card = dbc.Card(
		[
			html.Div(id = 'physician-patient-tempdata', style = {"display":"none"}),
			status(),
			list_header(),

			dbc.CardBody(
				[
					html.Div(id="physician-patient-list"),
				],
				id = 'physician-card-patient',
				style={"overflow-y":"scroll"}
			),       
		],
		style={"height":"120vh", "margin-top":"-2rem"}
	)

	return card

def list_header():
	return html.Div(
			[

				dbc.Row(
					[
						dbc.Col(html.H1("Patient List", style={"font-size":"2rem","color":"#000"})),
						dbc.Col(),
						dbc.Col(
							[
								# dbc.Badge("Sort By", pill=True, color="primary", className="mr-1"),
								html.H1("Sort By", style={"width":"6rem","margin-top":"0.5rem","font-size":"0.8rem","padding-left":"1rem"}),
								dbc.Select(
									id = 'physician-select-sorting',
									options = [
										{"label":"Patient Name", "value":0},
										{"label":"Assessments to be Reviewed", "value":5},
									],
									value = 5,
									bs_size = 'sm',
									style={"border-radius":"10rem","font-family":"NotoSans-Regular","font-size":"0.8rem"}
								)
							],
							# style={"display":"flex"}
						),
					],
					style={"text-align":"start","padding-bottom":"50px"},
				),
				dbc.Row(
					[
						dbc.Col(
							html.Div(
								html.H4("Patient Name", style={"font-size":"0.7rem","color":"#919191"})
							),
							width=2
						),
						dbc.Col(
							html.Div(
								html.H4("DOB", style={"font-size":"0.7rem","color":"#919191"})
							),
							width=2
						),
						dbc.Col(
							html.Div(
								html.H4("Age", style={"font-size":"0.7rem","color":"#919191"})
							),
							width=1
						),
						dbc.Col(
							html.Div(
								html.H4("Gender", style={"font-size":"0.7rem","color":"#919191"})
							),
							width=1
						),
						dbc.Col(
							html.Div(
								html.H4("Current Assessment", style={"font-size":"0.7rem","color":"#919191"})
							),
							width=2
						),
						dbc.Col(
							html.Div(
								html.H4("Assessments to be Reviewed", style={"font-size":"0.7rem","color":"#919191"})
							),
							width=2
						),
						dbc.Col(
							html.Div(
								html.H4("Review Due Date", style={"font-size":"0.7rem","color":"#919191"})
							),
							width=2
						),
					]
				),
				html.Hr(style={"margin-top":"-0.1rem"}),
			],
			style={"padding-left":"11rem","padding-right":"11rem","padding-top":"2rem","text-align":"center"}
		)


def status():
	return html.Div(
				html.Div(
					[
						html.Div(
							html.H1("Overview", style={"font-size":"2rem","color":"#000"}),
							style={"text-align":"start","padding-bottom":"0rem"},
						),
						html.Div(
							[
								html.Div(
									html.Div(
										[
											html.H6("TOTAL PATIENT ASSIGNED", style={"color":"#fff","width":"7rem"}),
											dbc.Badge("", id = 'physician-badge-patientct',style={"font-family":"NotoSans-SemiBold","font-size":"1.2rem","border-radius":"10rem","width":"4.5rem","background":"#fff","color":"#1357dd"}),
										],
										style={"border-radius":"0.8rem", "border":"1px solid #1357dd","background":"#1357dd","padding":"0.5rem","box-shadow":"0 4px 8px 0 rgba(19, 86, 221, 0.4), 0 6px 20px 0 rgba(19, 86, 221, 0.1)"}
									),
									style={"padding":"1rem"}
								),
								html.Div(
									html.Div(
										[
											html.H6("TOTAL ACTIVE TASKS", style={"color":"#fff","width":"7rem"}),
											dbc.Badge("", id = 'physician-badge-activetasks', style={"font-family":"NotoSans-SemiBold","font-size":"1.2rem","border-radius":"10rem","width":"4.5rem","background":"#fff","color":"#dc3545"}),
										],
										style={"border-radius":"0.8rem", "border":"1px solid #dc3545","background":"#dc3545","padding":"0.5rem","box-shadow":"0 4px 8px 0 rgba(220, 53, 70, 0.4), 0 6px 20px 0 rgba(220, 53, 70, 0.1)"}
									),
									style={"padding":"1rem"}
								),
								
							], 
							style={"display":"flex"}
						),
					],
					style={"padding-top":"3rem", "padding-left":"11rem", "padding-bottom":"2rem", "background":"#f5f5f5"}
				)
				
			)

			

def list_patients():
	return html.Div(
			[
				patient_item(app),
			], 
			style={"width":"100%","padding-right":"6rem","padding-left":"2rem","overflow-y":"scroll"}
		)





app.layout = html.Div(
		[
			
			login_layout(app),
			
			dbc.Fade(
				physician_layout(app),
				id="fade-transition",
				is_in=True,
				style={"transition": "opacity 100ms ease"},
			),
		]
	)


@app.callback(
	[
		Output("login-collapse-check", "is_open"),
		Output("login-layout", "hidden"),
		Output("physician-layout", "hidden"),
	],
	[
		Input("login-button-submit", "n_clicks"),
		Input("logout-button", "n_clicks")
	],
	[
		State("login-input-username", "value"),
		State("login-input-password", "value")
	]
	)
def login_check(nin, nout, un, pw):
	ctx = dash.callback_context
	if ctx.triggered[0]['prop_id'].split('.')[0] == 'login-button-submit':
		if un == username and pw == password:
			return False, True, False
		else: 
			return True, False, True
	elif ctx.triggered[0]['prop_id'].split('.')[0] == 'logout-button':
		return False, False, True
	else:
		return False, False, True


# @app.callback(
#     [
#         Output("login-layout", "hidden"),
#         Output("physician-layout", "hidden"),
#     ],
#     [
#         Input("logout-button", "n_clicks")
#     ]
#     )
# def login_check(n, un, pw):
#     if n:
#         return True, False



@app.callback(
	Output("navbar-collapse", "is_open"),
	[Input("navbar-toggler", "n_clicks")],
	[State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
	if n:
		return not is_open
	return is_open

@app.callback(
	Output("physician-patient-tempdata","children"),
	[Input("physician-select-sorting","value"),
#	Input({"type": "physician-patient-store-detail", 'index': 0}, "children")
	]
	)
def refresh_patient_info(v):
	rd = datetime.datetime.now().date() + datetime.timedelta(days = 7)
	rd = str(datetime.datetime.strftime(rd, '%m/%d/%Y'))
	infos = [["Kevin Scott","3/1/1952",68,"M",2,2,rd,3, 0],["Rhianna Kenny","9/19/1964",55,"F",0,0,"--",1, 1],["Mary Kim","5/12/1968",52,"F",0,0,"--",2, 2],]

	

	if v:
		infos = sorted(infos, key = lambda x: x[int(v)], reverse = True)

	physician_patient_tempdata = dict(patient_info=infos)
	return json.dumps(physician_patient_tempdata)

@app.callback(
		[
			Output("physician-patient-list", "children"),
			Output('physician-badge-patientct', 'children'),
		],
		[
			Input("physician-patient-tempdata", 'children'),
		]
	)
def update_patient_card(info):
	physician_patient_tempdata = json.loads(info)
	infos = physician_patient_tempdata['patient_info']

	patient_assessment_detail = [ ["Functional Assessment","Berg Balance Scale","Self Recording",str(datetime.datetime.now().date().strftime('%m/%d/%Y')),"Start Review", 0, 0],["Functional Assessment","Berg Balance Scale","Self Recording","04/01/2020","50", 0, 1],["Functional Assessment","Berg Balance Scale","Self Recording","01/01/2020","45", 0, 2],["Patient Health Status","KCCQ-12","Questionnaire",str(datetime.datetime.now().date().strftime('%m/%d/%Y')),"Start Review", 0, 3],["Patient Health Status","KCCQ-12","Questionnaire","04/15/2020","75", 0, 4],["Patient Health Status","KCCQ-12","Questionnaire","01/15/2020","69", 0, 5] ]

	patient_list = [

			html.Div(patient_item(app, *patient)) for patient in infos
			
	] + [
			html.Div(patient_data(patient_assessment_detail, patientid)) for patientid in [item[8] for item in infos]
	]
	return patient_list, len(infos)


@app.callback(
	Output({"type": "physician-modal-patient", 'index': MATCH}, "is_open"),
	[Input({"type": "physician-open-patient", 'index': MATCH}, "n_clicks"), Input({"type": "physician-close-patient", 'index': MATCH}, "n_clicks")],
	[State({"type": "physician-modal-patient", 'index': MATCH}, "is_open")],
	)
def toggle_modal_patient_item(n1, n2, is_open):
	if n1 or n2:
		return not is_open
	return is_open

@app.callback(
	Output({'type':'physician-modal-patient-modalbody', 'index':MATCH}, "children"),
	[Input({'type':'physician-modal-select-sorting', 'index':MATCH}, "value"),
	Input({"type": "physician-patient-store-detail", 'index': MATCH}, 'children')
	],
	[State({'type':'physician-modal-select-sorting', 'index':MATCH}, "id")]
	)
def update_review_assessment(v, data, id):
	patient_assessment_detail = json.loads(data)
	patient_assessment_detail_filtered = patient_assessment_detail['patient_data']
#	print('patient_assessment_detail', patient_assessment_detail_filtered)
#	patient_assessment_detail = load_data['detaildata']
	
	if v:
		patient_assessment_detail_filtered = sorted(patient_assessment_detail_filtered, key = lambda x: x[int(v)], reverse = True)

	patient_assessment_list = [
	  physician_assessment_item(*assessment) for assessment in patient_assessment_detail_filtered
	]

	return patient_assessment_list

@app.callback(
	Output({"type": "physician-assessment-collapse", 'index': MATCH}, "is_open"),
	[Input({"type": "physician-assessment-open-item", 'index': MATCH}, "n_clicks"), Input({"type": "physician-assessment-collapse-close", "index":MATCH}, "n_clicks")],
	[State({"type": "physician-assessment-collapse", 'index': MATCH}, "is_open")],
	)
def toggle_modal_patient_item(n1, n2,  is_open):
	if n1 or n2:
		return not is_open
	return is_open

@app.callback(
	[Output({"type": "physician-assessment-open-item", 'index': MATCH}, "children")],
	[Input({"type": "physician-assessment-collapse-close", "index":MATCH}, "n_clicks")],
	[State({"type": "physician-assessment-open-item", 'index': MATCH}, "children"),
	State({"type": "physician-assessment-collapse-score", 'index': MATCH}, "children")]
	)
def update_button_children(n, children, score):
	if children == "Start Review" and n:
		return [score]
	else:
		return [children]


@app.callback(
	Output({"type": "physician-patient-store-detail", 'index': 0}, 'children'),
	[Input({"type": "physician-assessment-open-item", 'index': ALL}, "children")],
	[State({"type": "physician-patient-store-detail", 'index': 0}, 'children')]
	)
def update_button_children(children, data):
	

	patient_assessment_detail=json.loads(data)['patient_data']

	
	for i in range(len(children)):
		patient_assessment_detail[i][4] = children[i]



	data_0 = json.dumps(dict(patient_data=patient_assessment_detail))

	return data_0

@app.callback(
	Output({"type": "physician-patient-assessments_2breviewed", 'index': 0}, 'children'),
	[Input({"type": "physician-patient-store-detail", 'index': 0}, 'children')]
	)
def update_2breviewed(data):
	patient_assessment_detail=json.loads(data)['patient_data']
#	if len(patient_assessment_detail)>0:
	to_assess = [item[4] for item in patient_assessment_detail].count('Start Review')
	
	return str(to_assess)

@app.callback(
	Output('physician-badge-activetasks', 'children'),
	[Input({"type": "physician-patient-assessments_2breviewed", 'index': ALL}, 'children')]
	)
def update_active(data):
	count = [0 if item == "--" else int(item)for item in data ]
#	count = list(map(int,data))
	active = sum(item for item in count)
	return str(active)


@app.callback(
	[Output({'type':'container-berg-scale-question-content','index':f'{i+1}'}, "hidden") for i in range(14)]
	+[Output("berg-scale-question-next", "disabled")],
	[Input({'type':'berg-scale-question','index':ALL}, "n_clicks")]
	+[Input("berg-scale-question-next", "n_clicks"),],
	[State({'type':'container-berg-scale-question-content','index':ALL}, "hidden")
	],
	)
#def switch_questions(q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14, next,qc1,qc2,qc3,qc4,qc5,qc6,qc7,qc8,qc9,qc10,qc11,qc12,qc13,qc14):
def switch_questions(q, next,qc):

	disable=False
	ctx = dash.callback_context

	if ctx.triggered[0]['prop_id'].split('.')[0] == 'berg-scale-question-next':

#        qc=[qc1,qc2,qc3,qc4,qc5,qc6,qc7,qc8,qc9,qc10,qc11,qc12,qc13,qc14]
		selected_index=[j for j, e in enumerate(qc) if e == False]
		num=selected_index[0]
		if num==12:
			disable=True
			qc[12]=True
			qc[13]=False
		elif num==13:
			disable=True
			qc[13]=False
		else: 
			disable=False
			qc[num]=True
			qc[num+1]=False

	else:
		qc=[True]*14
		triggered_button=ctx.triggered[0]['prop_id'].split('.')[0]
		if triggered_button=='':
			qc[0]=False
		else:
			num=int(triggered_button[10:12].replace('"',''))            
			qc[num-1]=False
			if num==14:
				disable=True
			else:
				disable=False

	
	return qc[0], qc[1], qc[2],qc[3],qc[4],qc[5],qc[6],qc[7],qc[8],qc[9],qc[10], qc[11], qc[12],qc[13],disable

@app.callback(
	[Output("berg-scale-score", "children"),
	Output({"type": "physician-assessment-collapse-score", 'index':'0-0'},"children")],
	[Input({'type':'berg-scale-question-content','index':ALL}, "value")]
	)
def cal_score(q):
	pl = list(filter(None, q))
	if len(pl)==0:
		score=0
	else:
		score=sum(pl)
	return 'Total Score: '+str(score)+'/56', str(score)

@app.callback(
	[Output({'type':'berg-scale-question','index':MATCH}, "color")],
	[Input({'type':'berg-scale-question-content','index':MATCH}, "value")]
	)
def update_style(v):
	# v = [v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14]
	# color = ['light'] * 14
	# for i in range(len(v)):
	# 	if v[i] is not None:
	# 		color[i] = 'primary'
	# return color[0],color[1],color[2],color[3],color[4],color[5],color[6],color[7],color[8],color[9],color[10],color[11],color[12],color[13]		
	if v is not None:
		return ['primary']
	else:
		return ['light']

if __name__ == "__main__":
	app.run_server(host="0.0.0.0",port=8094)

