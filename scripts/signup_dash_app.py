#!/usr/bin/env python3

import dash
from dash.dependencies import Input, Output

from fire_coverage.dashboard.serve_layout import serve_layout

app = dash.Dash('Fire Dash')
app.layout = serve_layout()
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

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
        result = 'Thanks {}!\n'.format(member_name)
        result += 'You are signed up for the following shifts:\n'
        return result + ', '.join(map(str, dates))
    else:
        return 'No member selected'

app.run_server(debug=True)
