# -*- coding: utf-8 -*-
from datetime import datetime as dt
import dash_core_components as dcc
import dash_html_components as html

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['fire_coverage']
member_list = [d['name'] for d in db.members.find()]

member_list_dropdown = dcc.Dropdown(id = 'member-list-dropdown',
                                    options = [{'label': i, 'value': i} for i in member_list],
                                    placeholder = 'Member Selection')

date_range = \
             html.Div([
                 html.H6('Select a date range'),
                 dcc.DatePickerRange(id = 'date-range',
                                     minimum_nights = 0,
                                     initial_visible_month = \
                                     dt.now())])

operation = dcc.RadioItems( id='date-operation',
    options=[
        {'label': 'Select', 'value': 'add'},
        {'label': 'Clear', 'value': 'clear'},
        {'label': 'Deselect', 'value': 'remove'},
    ],
    value='add',
    labelStyle={'display': 'inline-block'}
)

single_date = \
             html.Div([
                 html.H6('Date Selection'),
                 operation,
                 dcc.DatePickerSingle(id = 'single-date',
                                     initial_visible_month = \
                                      dt.now())]
             )

print(dt.now())
calendar = html.Div([html.Div([html.Button('<', id='previous-month-button', className = 'four columns'),
                              html.Div('June', id='current-month', className = 'four columns'),
                               html.Button('>', id='next-month-button', className = 'four columns')],
                              className = 'row'),
                     html.Div([html.Button('<', id='previous-year-button', className = 'four columns'),
                               html.Div('2019', id='current-year', className = 'four columns'),
                               html.Button('>', id='next-year-button', className = 'four columns')],
                              className = 'row'),
                     html.Table(id='calendar-table', style = {'display': 'inline-block'})],
                    style = {'width' : '100%'})

header_pane = html.Div([html.H1("Nederland Fire Protection District"),
                        html.H2("Volunteer Night Coverage Sign Up"),
                        html.Hr(),                        
                        member_list_dropdown,
                        html.Hr(),
                        calendar,
                        single_date,                             
                        html.Div(id='dates-selected'),
                        html.Hr(),
                        html.Button('SignUp', id='signup-button'),
                        html.Div(id='signed-up')],
                       style = {'textAlign': 'center'})    


