import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
from dash import no_update

from flask_login import login_user, current_user
from werkzeug.security import check_password_hash
import time

from server import app, User


success_alert = dbc.Alert(
    'Logged in successfully',
    color='success',
    dismissable=True
)
failure_alert = dbc.Alert(
    'Login unsuccessful. Try again.',
    color='danger',
    dismissable=True
)
already_login_alert = dbc.Alert(
    'User already logged in',
    color='warning',
    dismissable=True
)


# def layout():
#     return dbc.Row(
#         dbc.Col(
#             [
#                 dcc.Location(id='login-url',refresh=True,pathname='/login'),
#                 html.Div(id='login-trigger',style=dict(display='none')),
#                 html.Div(id='login-alert'),
#                 dbc.FormGroup(
#                     [
#                         # dbc.Alert('Try test@test.com / test', color='info',dismissable=True),
#                         # html.Br(),

#                         dbc.Input(id='login-username',autoFocus=True),
#                         dbc.FormText('Username'),
                        
#                         html.Br(),
#                         dbc.Input(id='login-password',type='password'),
#                         dbc.FormText('Password'),
                        
#                         html.Br(),
#                         dbc.Button('Submit',color='primary',id='login-button'),
#                         #dbc.FormText(id='output-state')
                        
#                         html.Br(),
#                         html.Br(),
#                         dcc.Link('Register',href='/register'),
#                         html.Br(),
#                         dcc.Link('Forgot Password',href='/forgot')
#                     ]
#                 )
#             ],
#             width=6
#         )
#     )


def layout():
    return html.Div(
                [
                    dcc.Location(id='login-url',refresh=True,pathname='/login'),
                    html.Div(id='login-trigger',style=dict(display='none')),
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
                                        # dbc.Collapse(children = ["\u2757", "Please check your username and password."],
                                        #     id = 'login-collapse-check',
                                        #     is_open = False,
                                        #     style={"text-align":"center"}
                                        #     ),
                                        html.Div(id='login-alert'),
                                        html.Div(
                                            [
                                                html.Form(
                                                    [
                                                        html.Div(
                                                            dbc.Input(placeholder="Username", type="text", style={"border-radius":"10rem"}, id = "login-username"),
                                                            style={"padding":"0.5rem"}
                                                        ),
                                                        html.Div(
                                                            dbc.Input(placeholder="Password", style={"border-radius":"10rem"}, type = 'password', id = "login-password"),
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
                                                                            id = "login-button"
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
                                                    # action='/login', 
                                                    # method='post'
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
                style={"background":"url(./assets/patient-login.png)","height":"100vh"},
                id="login-layout"
            )



@app.callback(
    [Output('login-url', 'pathname'),
     Output('login-alert', 'children')],
    [Input('login-button', 'n_clicks')],
    [State('login-username', 'value'),
     State('login-password', 'value')]
)
def login_success(n_clicks, username, password):
    '''
    logs in the user
    '''
    if n_clicks:
        ####!!!change here!!!#####
        user = User.query.filter_by(email=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)

                return '/home',success_alert
            else:
                return no_update,failure_alert
        else:
            return no_update,failure_alert
    else:
        return no_update,''