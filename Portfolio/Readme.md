Road map:

- Load multiple ticker data feed
- DataAdapter: Component handles lines in Backtrader: make a nice pandas DataFrame
- Portfolio: Component configures pypfopt's optimizer
- OrderGenerator: Component handles weights: Send order to Backtrader's system

In the `next` function of the strategy, all the data feed is passed to `DataAdapter`, it will then produce a pandas
 DataFrame, which contains all the data till t-0. (In Backtrader's system, 0 means now, -1 means T-1..) 
 
`Portfolio` wraps an optimizer. It consumes DataFrame from `DataAdapter` and produces weights and diatonic info.

`OrderGenerator` generates orders given current position, current prices, and new target weights, which is generated
 by `Portfolio`. 
 
Backtrader seems already have a weights based strategy.
