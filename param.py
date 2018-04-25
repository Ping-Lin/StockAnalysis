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
RSS_CH_SEARCH_URL = 'http://tw.stock.yahoo.com/rss/q/'
