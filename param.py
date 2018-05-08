# for stockretriever.py
PUBLIC_API_URL = 'http://query.yahooapis.com/v1/public/yql'
DATATABLES_URL = 'store://datatables.org/alltableswithkeys'
HISTORICAL_URL = 'http://ichart.finance.yahoo.com/table.csv?s='
RSS_URL = 'http://finance.yahoo.com/rss/headline?s='
FINANCE_TABLES = {
    'quotes': 'yahoo.finance.quotes',
    'options': 'yahoo.finance.options',
    'quoteslist': 'yahoo.finance.quoteslist',
    'sectors': 'yahoo.finance.sectors',
    'industry': 'yahoo.finance.industry'
}

# for chineseStockRetriever.py use
RSS_CH_STOCK_SEARCH_URL = 'http://tw.stock.yahoo.com/rss/q/'

# this will be N1.html N2.html ...
# reference: https://tw.finance.yahoo.com/rss_index.html#listings
RSS_CH_NEWS_SEARCH_URL = 'https://tw.finance.yahoo.com/rss/url/d/e/N'
