import datetime
from WindPy import w
w.start()
w.isconnected()


def load_cpi(start_d="1987-01-31", end_d=datetime.date.today().strftime("%Y-%m-%d")):
    error_code, rtn = w.edb("M0000612", start_d, end_d,"Fill=Previous", usedf=True)
    rtn.rename(columns={'CLOSE': 'cpi'}, inplace=True)
    rtn = rtn['cpi'] / 100
    return rtn


if __name__ == '__main__':
    load_cpi()
