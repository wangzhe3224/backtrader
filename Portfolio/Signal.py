import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data = pd.read_csv('/home/wz/Projects/research/notebooks/data/us_etf_tr.csv', index_col='Unnamed: 0', parse_dates=True)
price = pd.read_csv('/home/wz/Projects/research/notebooks/data/us_etf_pr.csv', index_col='Unnamed: 0', parse_dates=True)
vix = pd.read_csv('~/vix.csv', index_col='Unnamed: 0', parse_dates=True)
signal = pd.read_csv('~/signal.csv', index_col='Unnamed: 0', parse_dates=True)
selected = ['SPY', 'TLT']

total_return = data.dropna()[selected]
total_return = total_return.reindex(signal.index)
init_date = total_return.index[0]

all_dates = total_return.index


def need_rebalance(date, idx, df):
    """ do we rebalance? """
    return True


threshold = 0.1
large = 0.7
small = 1-large

weights_hist = {}
for idx, date in enumerate(all_dates):

    cur_signal = signal.avg_label.loc[date]
    if np.isnan(cur_signal):
        continue

    if cur_signal < threshold:
        weights_hist[date] = {'TLT': small, 'SPY': large}
    else:
        weights_hist[date] = {'TLT': large, 'SPY': small}

## Post process
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
# plt.show()
print('Done.')

weight_df.iloc[:].plot()
# plt.show()

pnls.plot()
# Statistics
print(ret.describe())
print('Mean: ', ret.mean()*252)
print('Std: ', ret.std()*252**0.5)