def order(security, amount, style=OrderType):
    pass

def order_value(security, amount, style=OrderType):
    pass

def order_percent(security, amount, style=OrderType):
    pass

def order_target(security, amount, style=OrderType):
    pass

def order_target_value(security, amount, style=OrderType):
    pass

def order_target_percent(security, percent, style=type):
    pass

def cancel_order(order):
    pass

def get_open_orders(sid=sid):
    pass

def get_order(order):
    pass

def get_fundamentals(query, filter_ordered_nulls):
    pass

def order(security, amount, style=RelativeOrder(offset, pct_offset, limit_price, exchange)):
    pass

def order(security, amount, style=VWAPBestEffort(limit_price=price1, start_date=date1,
end_date=date2, max_pct_vol=percent,
avoid_liquidity=False, exchange=Exchange)):
    pass