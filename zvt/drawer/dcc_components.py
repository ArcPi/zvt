# -*- coding: utf-8 -*-

import dash_core_components as dcc
import plotly.graph_objs as go

from zvt.api.business import get_orders
from zvt.api.business_reader import OrderReader, AccountStatsReader
from zvt.api.quote import decode_entity_id
from zvt.factors.technical_factor import TechnicalFactor
from zvt.utils.pd_utils import pd_is_not_null


def get_account_figure(account_reader: AccountStatsReader):
    account_data, account_layout = account_reader.draw(render=None, value_fields='all_value')

    return go.Figure(data=account_data, layout=account_layout)


def order_type_color(order_type):
    if order_type == 'order_long' or order_type == 'order_close_short':
        return "#ec0000"
    else:
        return "#00da3c"


def order_type_flag(order_type):
    if order_type == 'order_long' or order_type == 'order_close_short':
        return 'B'
    else:
        return 'S'


def get_trading_signals_figure(order_reader: OrderReader,
                               entity_id: str,
                               provider: str,
                               level):
    entity_type, _, _ = decode_entity_id(entity_id)
    security_factor = TechnicalFactor(entity_type=entity_type, entity_ids=[entity_id],
                                      level=level, provider=provider)

    if pd_is_not_null(security_factor.data_df):
        print(security_factor.data_df.tail())

    # generate the annotation df
    order_reader.move_on(timeout=0)
    df = order_reader.data_df.copy()
    if pd_is_not_null(df):
        df['value'] = df['order_price']
        df['flag'] = df['order_type'].apply(lambda x: order_type_flag(x))
        df['color'] = df['order_type'].apply(lambda x: order_type_color(x))
    print(df.tail())

    data, layout = security_factor.draw(render=None, figures=go.Candlestick, annotation_df=df)

    return go.Figure(data=data, layout=layout)


def get_account_stats_figure(account_stats_reader: AccountStatsReader):
    graph_list = []

    # 账户统计曲线
    if account_stats_reader:
        fig = account_stats_reader.draw_line(show=False)

        for trader_name in account_stats_reader.trader_names:
            graph_list.append(dcc.Graph(
                id='{}-account'.format(trader_name),
                figure=fig))

    return graph_list

def get_trading_entities(trader_name:str):
    order:Order=get_orders(trader_name=trader_name,return_type='domain')