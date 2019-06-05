#!/usr/bin/env python3

import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from serve_layout import serve_layout

app = dash.Dash('Fire Dash')
app.layout = serve_layout()

dates = set()

@app.callback(
    Output(component_id='dates-selected', component_property='children'),
    [Input(component_id='single-date', component_property='date'),
     Input(component_id='date-operation', component_property='value')]
)
def update_output_div(single_date, op):
    if op == 'clear':        
        dates.clear()
    if single_date:
        if op == 'add':        
            dates.add(single_date)
        if op == 'remove':        
            dates.remove(single_date)
    return ', '.join(map(str, dates))

@app.callback(
    Output(component_id='signed-up', component_property='children'),
    [Input(component_id='signup-button', component_property='n_clicks'),
     Input(component_id='member-list-dropdown', component_property='value')]
)
def signup(n_clicks, member_name):

    if member_name:

        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/')
        db = client['fire_coverage']

        for d in dates:
            year = int(d.split('-')[0])
            month = int(d.split('-')[1])
            day = int(d.split('-')[2])

            dt = datetime.datetime(year, month, day)
            document = db.signups.find_one({'datetime': dt})

            if not document:
                result = db.signups.insert({'datetime': dt,
                                            'members_on_shift': [member_name]})
            else:
                document['members_on_shift'].append(member_name)
                result = db.signups.update_one({'_id': document['_id']},
                                               {'$set': document})

            print(result)

        result = 'Thanks {}!\n'.format(member_name)
        result += 'You are signed up for the following shifts:\n'
        return result + ', '.join(map(str, dates))
    else:
        return 'No member selected'

@app.callback(Output('current-month', 'children'),
              [Input('previous-month-button', 'n_clicks_timestamp'),
               Input('next-month-button', 'n_clicks_timestamp')],
              [State('current-month', 'children')]
)              
def change_month(previous_month_click_timestamp,
               next_month_click_timestamp,
               current_month):

    months = ['January',
              'February',
              'March',
              'April',
              'May',
              'June',
              'July',
              'August',
              'September',
              'October',
              'November',
              'December']

    previous_month_click_timestamp = 0 if not previous_month_click_timestamp else previous_month_click_timestamp 
    next_month_click_timestamp = 0 if not next_month_click_timestamp else next_month_click_timestamp     
    
    month_index = months.index(current_month)
    if previous_month_click_timestamp > next_month_click_timestamp:       
        month_index -= 1

    if next_month_click_timestamp > previous_month_click_timestamp:
        month_index += 1
        
    month_index = max(0, min(month_index, len(months)-1))
    return months[month_index]

@app.callback(Output('current-year', 'children'),
              [Input('previous-year-button', 'n_clicks_timestamp'),
               Input('next-year-button', 'n_clicks_timestamp')],
              [State('current-year', 'children')]
)              
def change_year(previous_year_click_timestamp,
                next_year_click_timestamp,
                current_year):

    previous_year_click_timestamp = 0 if not previous_year_click_timestamp else previous_year_click_timestamp 
    next_year_click_timestamp = 0 if not next_year_click_timestamp else next_year_click_timestamp     

    if previous_year_click_timestamp > next_year_click_timestamp:       
        current_year = int(current_year) - 1

    if next_year_click_timestamp > previous_year_click_timestamp:
        current_year = int(current_year) + 1

    return max(2019, int(current_year))
        
@app.callback(Output('calendar-table', 'children'),
              [Input('current-month', 'children'),
               Input('current-year', 'children')])
def generate_calendar(current_month, current_year):

    import random
    import calendar

    from pymongo import MongoClient
    client = MongoClient('mongodb://localhost:27017/')
    db = client['fire_coverage']

    member_names = [d['name'] for d in db.members.find()]
    
    months = ['January', 'February', 'March', 'April',              
              'May', 'June', 'July', 'August', 'September',              
              'October', 'November', 'December']
    
    month = months.index(current_month) + 1
    year = int(current_year)
    
    cal = calendar.monthcalendar(year, month)

    days = ['Mon', 'Tues', 'Weds', 'Thurs', 'Fri', 'Sat', 'Sun']
    header = [html.Tr([html.Th(day) for day in days])]
    body = list()

    for week in cal:
        row = list()
        for day in week:
            if day:
                day_header = html.Tr([html.Th(day)])
                
                dt = datetime.datetime(year, month, day)                
                shift_document = db.signups.find_one({'datetime': dt})

                members_on_shift_rows = [day_header]
                if shift_document:
                    for member_name in shift_document['members_on_shift']:
                        print("Thank you for your service, %s" % member_name)
                        members_on_shift_rows.append(html.Tr([html.Td(member_name)]))
                else:                    
                    members_on_shift_rows.append(html.Tr([html.Td('---')]))

                day_table = html.Table(members_on_shift_rows)
                row.append(html.Td(day_table))
            else:
                row.append(html.Td())
        body.append(html.Tr(row))
            
    return html.Table(header + body)
    
app.run_server(debug=True)


