import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

import base64
import cv2
import datetime
import os
import pandas as pd
import numpy as np

import pathlib
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
from server import app, server

from flask_login import logout_user, current_user


def modal_self_recording_review_prior(app, filename, score, num):
	submit_date = filename.split('_')[0]
	d = submit_date.split('-')[1]+'/'+submit_date.split('-')[2]+'/'+submit_date.split('-')[0]
	path = str('configure/') + current_user.email +str('/upload/') + filename
	encoded_video = base64.b64encode(open(path, 'rb').read())
	cap = cv2.VideoCapture(path) 
	
	if cap.isOpened():
		rate = cap.get(5)
		FrameNumber = cap.get(7)
		duration = int(FrameNumber/rate)

	size = round(os.path.getsize(path)/(1024*1024),1)

	return html.Div(
				[
					html.H6("Review", style={"font-size":"0.7rem","padding-top":"10px"}),
					dbc.Button(children = [html.Img(src=app.get_asset_url("icon-laptop-play-video-100.png"), style={"height":"1.5rem", "padding-top":"0px"})], color="light",style={"border-radius":"10rem"}, id = u'video-modal-review-prior-button-open-{}'.format(num)),
					dbc.Modal(
						[
							dbc.ModalHeader(
								html.Div(
									[
										html.H1("Berg Balance Scale",style={"font-size":"1.5rem"}),
										dbc.Badge(d + " Completed", color="primary", className="mr-1",style={"font-family":"NotoSans-SemiBold","font-size":"1rem"}),
										html.Div(style={"height":"20px"}),
										dbc.Row(
											[
												dbc.Col(
													[
														html.H6("File Name : "+ filename),
														html.H6("Duration : "+ str(duration)+' s'),
														html.H6("Size : "+ str(size)+' MB'),
													]
												),
												dbc.Col(
													html.Div(
														[
															dbc.Badge("Total Score: ", color="warning", className="mr-1",style={"font-family":"NotoSans-SemiBold","font-size":"0.8rem"}),
															html.H1(score + "/56", style={"font-size":"2rem","color":"#ffc107"}),
														]
													)
													
												),
											],
											style={"width":"1600px"}
										)
									],
                            		style={"padding-left":"40px","padding-right":"40px","padding-top":"10px","padding-bottom":"10px"}
								)
							),
							dbc.ModalBody(
								html.Div(
									[
										html.Video(src='data:image/png;base64,{}'.format(encoded_video.decode()), controls = True, style={"height":"25rem","border-bottom":"none", "text-align":"center"} ),
									],
									style={"text-align":"center"}
								)
							),
							dbc.ModalFooter(
								dbc.Button("close", id=u"video-modal-review-prior-button-submit-{}".format(num), className="mr-2"),
							)
						],
						id = u"modal-selfrecording-review-prior-{}".format(num),
						size = 'xl',
						backdrop = "static"
					)
				]
			)



