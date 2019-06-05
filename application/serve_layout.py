# -*- coding: utf-8 -*-
import datetime
import dash_core_components as dcc
import dash_html_components as html

from header_pane import header_pane

def serve_layout():
    return html.Div([header_pane])
