# -*- coding: utf-8 -*-
from typing import List

from zvt.contract.api import get_group, get_data
from zvt.schemas import business
from zvt.schemas.business import AccountStats, Position, Order
from zvt.utils.pd_utils import pd_is_not_null


def get_traders() -> List[str]:
    df = get_group(provider='zvt', data_schema=AccountStats, column=AccountStats.trader_name, group_func=None)
    if pd_is_not_null(df):
        return df['trader_name'].tolist()
    return []


def get_trader(trader_name=None, return_type='df', start_timestamp=None, end_timestamp=None,
               filters=None, session=None, order=None, limit=None) -> List[business.SimAccount]:
    if trader_name:
        if filters:
            filters = filters + [business.SimAccount.trader_name == trader_name]
        else:
            filters = [business.SimAccount.trader_name == trader_name]

    return get_data(data_schema=business.SimAccount, entity_id=None, codes=None, level=None, provider='zvt',
                    columns=None, return_type=return_type, start_timestamp=start_timestamp,
                    end_timestamp=end_timestamp, filters=filters, session=session, order=order, limit=limit)


def get_account(trader_name=None, return_type='df', start_timestamp=None, end_timestamp=None,
                filters=None, session=None, order=None, limit=None):
    if trader_name:
        if filters:
            filters = filters + [AccountStats.trader_name == trader_name]
        else:
            filters = [AccountStats.trader_name == trader_name]

    return get_data(data_schema=AccountStats, entity_id=None, codes=None, level=None, provider='zvt',
                    columns=None, return_type=return_type, start_timestamp=start_timestamp,
                    end_timestamp=end_timestamp, filters=filters, session=session, order=order, limit=limit)


def get_position(trader_name=None, return_type='df', start_timestamp=None, end_timestamp=None,
                 filters=None, session=None, order=None, limit=None):
    if trader_name:
        if filters:
            filters = filters + [Position.trader_name == trader_name]
        else:
            filters = [Position.trader_name == trader_name]

    return get_data(data_schema=Position, entity_id=None, codes=None, level=None, provider='zvt',
                    columns=None, return_type=return_type, start_timestamp=start_timestamp,
                    end_timestamp=end_timestamp, filters=filters, session=session, order=order, limit=limit)


def get_orders(trader_name=None, return_type='df', start_timestamp=None, end_timestamp=None,
               filters=None, session=None, order=None, limit=None):
    if trader_name:
        if filters:
            filters = filters + [Order.trader_name == trader_name]
        else:
            filters = [Order.trader_name == trader_name]

    return get_data(data_schema=Order, entity_id=None, codes=None, level=None, provider='zvt',
                    columns=None, return_type=return_type, start_timestamp=start_timestamp,
                    end_timestamp=end_timestamp, filters=filters, session=session, order=order, limit=limit)


if __name__ == '__main__':
    print(get_trader())
