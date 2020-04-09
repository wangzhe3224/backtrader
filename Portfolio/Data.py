import requests
import datetime
import calendar

import pandas as pd


def dateToUnix(dt: str) -> int:
    """ change date str into a unix time stamp in UTC

    :param dt: YYYY-MM-DD
    :return:
    """
    _d = datetime.datetime.strptime(dt, '%Y-%m-%d')
    unixtime = calendar.timegm(_d.timetuple())

    return int(unixtime)


def getData(ticker: str, field: str, start: str, end: str, cur: str,
            url: str='http://dataapi.eu.ngrok.io.eu.ngrok.io') -> pd.DataFrame:
    """ Get data from DataAPI return a pandas dataframe

    :param ticker:
    :param field:
    :param start:
    :param end:
    :param cur:
    :return:
    """
    startint = dateToUnix(start)
    endint = dateToUnix(end)
    reqUrl = url + '/data/bbg/getAssetsHistoryStartEnd/[{ticker}]/[{field}]/{s}/{t}/{cur}'.format(
        ticker=ticker, field=field, s=startint, t=endint, cur=cur
    )
    res = requests.get(reqUrl)
    data = pd.DataFrame.from_dict(res.json()[ticker][field], orient='index')
    data.index = pd.to_datetime(data.index, unit='s')

    return data


if __name__ == '__main__':

    etf = ['SPY', 'TLT', 'HYG', 'LQD', 'GLD', 'EEM', 'EMB', 'IYR', 'EFA']
    fields = ['PX_LAST', 'PX_OPEN', 'PX_HIGH', 'PX_LOW', 'PX_VOLUME']
    bbgs = [i + ' US Equity' for i in etf]
    tickers = ','.join(bbgs)
    fields_str = ','.join(fields)
    print(fields_str)

    start = '2000-01-01'
    end = datetime.datetime.now().strftime('%Y-%m-%d')
    for idx, ticker in etf:
        bbg_ticker = bbgs[idx]
        df = getData(bbg_ticker, 'PX_LAST', start, end, 'USD')

    data = getData(bbgs[0], fields_str, start, end, 'USD')
    print(data)