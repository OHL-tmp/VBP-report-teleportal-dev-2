# -*- coding: utf-8 -*-
"""
Created on Mon Jul 6 11:01:53 2020

@author: rongxu
"""

import pandas as pd
import plotly.graph_objects as go
import dash_table
from dash_table.Format import Format, Scheme
import dash_table.FormatTemplate as FormatTemplate

df_kccq_score=pd.read_csv("data/kccq_score.csv")

colors={'blue':'rgba(18,85,222,1)','yellow':'rgba(246,177,17,1)','transparent':'rgba(255,255,255,0)','grey':'rgba(191,191,191,1)',
       'lightblue':'rgba(143,170,220,1)'}
def data_process(df,current_score,submit_date):
    df.iloc[:,[3]]= current_score
    df=df.rename(columns={(df.columns[3]):submit_date+"(Current Assessment)"})    
    df.iloc[:,[4]]=df.iloc[:,3]-df.iloc[:,1]
    return df
   

def tbl(df):
    tbl=dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c,'type': 'numeric',"format":Format( precision=0,group=',', scheme=Scheme.fixed,),} for c in df.columns],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_data_conditional=[
            {'if': {'row_index':4},
             'backgroundColor':'rgba(225,225,225)',
            } 
        ],
        style_cell={
            'textAlign': 'center',
            'font-family':'NotoSans-Condensed',
            'fontSize':16,
            'backgroundColor':'rgba(245,245,245,1)'
        },
        style_cell_conditional=[
            {'if': {'column_id': df.columns[0]},
             'textAlign':'start',
             'width': '20rem',
             'font-family':'NotoSans-Condensed',
            },     
        ],
        style_header={
            'height': '4rem',
            'backgroundColor':'#f1f6ff',
            'fontWeight': 'bold',
            'font-family':'NotoSans-CondensedLight',
            'fontSize':14,
            'color': '#1357DD'
        },
    )
    
       
    return tbl


def bargraph(df): 

    colorbar=['rgba(191,191,191,0.7)','rgba(18,85,222,0.6)','rgba(18,85,222,0.8)']

    fig = go.Figure()

    for k in range(len(df.columns)-2):
        fig.add_trace(
            go.Bar(
            name=df.columns[k+1], 
            x=df.iloc[:,0].tolist(), 
            y=df.iloc[:,(k+1)].tolist(),
            text=df.iloc[:,(k+1)].tolist(),
            textposition='outside',
            texttemplate='%{y:.0f}',#'%{y:.2s}',
            constraintext='none',
            marker=dict(
                color=colorbar[k],
                       ),
#            hovertemplate='%{y:,.0f}',
            hoverinfo='skip',
            )
        )


    fig.update_layout(
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        barmode='group',
        showlegend=True,
        legend=dict(
            orientation='h',
            x=0.3,y=-0.05
        ),

        margin=dict(l=0,r=0,b=50,t=10,pad=0),
        font=dict(
            family="NotoSans-CondensedLight",
            size=12,
            color="#38160f"
        ),
        yaxis = dict(
            #showgrid = True, 
            #gridcolor =colors[3],
            showline=True,
            linecolor='grey',
            tickmode='linear',
            dtick=20,
            range=[0,100],
            showticklabels=True,
            zeroline=True,
            zerolinecolor='grey',
            ticks='inside'
        ),

#        hovermode=False,
        modebar=dict(
            bgcolor=colors['transparent']
        ),
    )
    return fig
