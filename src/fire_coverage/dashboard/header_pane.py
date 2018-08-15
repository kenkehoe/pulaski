# -*- coding: utf-8 -*-
from datetime import datetime as dt
import dash_core_components as dcc
import dash_html_components as html

member_list = ['Olivas', 'Kehoe']
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

header_pane = html.Div([html.H1("Nederland Fire Protection District"),
                        html.H2("Volunteer Night Shift Sign Up"),
                        html.Hr(),                        
                        member_list_dropdown,
                        html.Hr(),                        
                        single_date,                             
                        html.Div(id='dates-selected'),
                        html.Hr(),
                        html.Button('SignUp', id='signup-button'),
                        html.Div(id='signed-up')],
                       style = {'textAlign': 'center'})    


