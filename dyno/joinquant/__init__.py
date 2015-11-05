
def set_universe(security_list):
    pass

def get_industry_stocks(industry_code):
    pass

def get_index_stocks(index_symbol):
    pass

def order(security, amount, style=None):
    pass

def order_target(security, amount, style=None):
    pass

def cancel_order(order):
    pass

def get_open_orders():
    pass

def history(count, unit='1d', field='price', security_list=None):
    pass

def attribute_history(security, count, unit='1d', fields=('open', 'close', 'high', 'low', 'volume', 'money'), skip_paused=True):
    pass

def record(**kwargs):
    pass

def set_benchmark(security):
    pass

def set_commission(object):
    pass

def set_slippage(object):
    pass

def write_file(path, content):
    raise NotImplementedError()

def read_file(path):
    raise NotImplementedError()

class UserContext:
    pass

class SecurityUnitData:
    pass

class Portfolio:
    pass

class Position:
    pass

class Order:
    pass



class OrderStatus(Enum):
    open = 0
    filled = 1
    canceled = 2
    rejected = 3
    held = 4

class OrderStyle:
    pass


class MarketOrderStyle(OrderStyle):
    pass

class LimitOrderStyle(OrderStyle):
    def __init__(self, limit_price):
        self.limit_price = limit_price
    pass


def get_price(security, start_date='2015-01-01', end_date='2015-12-31', frequency='daily', fields=None):
    pass

def get_all_securities():
    pass

