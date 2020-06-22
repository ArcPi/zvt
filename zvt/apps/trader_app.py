# -*- coding: utf-8 -*-
from typing import List

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from zvt.api.business import get_trader_info
from zvt.api.business_reader import AccountStatsReader, OrderReader
from zvt.apps import app
from zvt.domain import TraderInfo
from zvt.drawer.dcc_components import get_account_stats_figure

account_readers = []
order_readers = []

# init the data
traders: List[TraderInfo] = get_trader_info(return_type='domain')

trader_names: List[str] = [item.trader_name for item in traders]


def load_traders():
    global traders
    global trader_names

    traders = get_trader_info(return_type='domain')
    for trader in traders:
        account_readers.append(AccountStatsReader(trader_names=[trader.trader_name], level=trader.level))
        order_readers.append(OrderReader(trader_names=[trader.trader_name]))

    trader_names = [item.trader_name for item in traders]


load_traders()


def serve_layout():
    layout = html.Div(
        [
            html.Div(
                [
                    dcc.Dropdown(
                        id='trader-selector',
                        placeholder='select the trader',
                        options=[{'label': item, 'value': i} for i, item in enumerate(trader_names)])
                ]),

            html.Div(id='trader-details', style={'width': '80%', 'margin': 'auto'}),

            dcc.Interval(
                id='interval-component',
                interval=5 * 1000,  # in milliseconds
                n_intervals=0
            )

        ])

    load_traders()

    return layout


@app.callback(
    Output('trader-details', 'children'),
    [Input('interval-component', 'n_intervals'),
     Input('trader-selector', 'value')])
def update_trader_details(n, i):
    if i is None or n < 1:
        return ''

    return get_account_stats_figure(account_stats_reader=account_readers[i])
