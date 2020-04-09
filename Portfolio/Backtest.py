import requests
import datetime
import calendar

import pandas as pd

from pypfopt.expected_returns import mean_historical_return, ema_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier

import matplotlib.pyplot as plt


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
    from pypfopt.hierarchical_portfolio import HRPOpt

    data = pd.read_csv('/home/wz/Projects/research/notebooks/data/us_etf_tr.csv', index_col='Unnamed: 0', parse_dates=True)
    price = pd.read_csv('/home/wz/Projects/research/notebooks/data/us_etf_pr.csv', index_col='Unnamed: 0', parse_dates=True)
    vix = pd.read_csv('~/vix.csv', index_col='Unnamed: 0', parse_dates=True)

    selectd = ['SPY', 'TLT', ]

    total_return = data.dropna()[selectd].loc['2011': ]
    init_date = total_return.index[0]
    vix = vix.reindex(total_return.index, method='ffill')

    LOOKBACK = 125
    RE_FREQ = int(1*252/12)
    U = 35
    L = 21
    global RISK_ON
    RISK_ON = False


    def need_rebalance(date, idx, vix):
        """"""
        global RISK_ON
        if idx % RE_FREQ == 0:
            return True
        if vix > U and not RISK_ON:
            print(date, 'Big vix and switch risk on')
            RISK_ON = True
            return True
        if vix < L and RISK_ON:
            print(date, 'Low vix, switch risk off')
            RISK_ON = False
            return True

    weights_hist = {}

    for idx, date in enumerate(total_return.index):
        pre_r = init_date
        vix_value = vix.iloc[idx]['VIX Index']
        if idx == 0:
            continue
        if need_rebalance(date, idx, vix_value):
            # if vix_value > 40:
            #     weights_hist[date] = {k: 0.0 for k in total_return.columns}
            #     continue
            df = total_return[date - datetime.timedelta(days=LOOKBACK): date]
            mu = ema_historical_return(df)
            S = CovarianceShrinkage(df, LOOKBACK).ledoit_wolf()
            # ef = EfficientFrontier(mu, S)
            ef = HRPOpt(df.pct_change())
            try:
                # ef.max_sharpe()
                ef.optimize()
                weights = ef.clean_weights()
                print(date, weights)
                weights_hist[date] = weights
            except:
                raise
                weights_hist[date] = {k: 0.0 for k in data.columns}

    # Construct weights
    weight_df = pd.DataFrame.from_dict(weights_hist).transpose()
    weight_df = weight_df.reindex(total_return.index, method='ffill').shift(1)

    # Calculate return
    ret_com = total_return.pct_change().mul(weight_df, axis=1)
    ret = ret_com.sum(axis=1)
    print(ret)
    pnl = ret.cumsum()
    print(pnl)
    pnls = ret_com.cumsum()
    pnl.iloc[:].plot()
    plt.show()
    print('Done.')

    weight_df.iloc[:].plot()
    plt.show()

    pnls.plot()
    plt.show()
    # Statistics
    print(ret.describe())
    print('Mean: ', ret.mean()*252)
    print('Std: ', ret.std()*252**0.5)
# def extend_pandas():
#     """
#     Extends pandas' PandasObject (Series, Series,
#     DataFrame) with some functions defined in this file.
#     This facilitates common functional composition used in quant
#     finance.
#     Ex:
#         prices.to_returns().dropna().calc_clusters()
#         (where prices would be a DataFrame)
#     """
#     PandasObject.to_returns = to_returns
#     PandasObject.to_log_returns = to_log_returns
#     PandasObject.to_price_index = to_price_index