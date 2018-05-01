from stockretriever import (
    StockRetriever,
    QueryError,
)
from param import (
    RSS_CH_SEARCH_URL
)


class ChineseStockRetriever(StockRetriever):
    def __init__(self):
        super(ChineseStockRetriever, self).__init__()

    def get_chinese_news_feed(self, symbol):
        """Retrieves the rss feed for the provided symbol."""

        feedUrl = RSS_CH_SEARCH_URL + symbol
        yql = 'select title, link, description, pubDate from rss ' \
              'where url=\'%s\'' % feedUrl
        response = super(ChineseStockRetriever, self).execute(yql)
        result = response['query']['results']['item'][0]['title']
        if result.find('not found') > 0:
            raise QueryError('Feed for %s does not exist.' % symbol)
        else:
            return response['query']['results']['item']
