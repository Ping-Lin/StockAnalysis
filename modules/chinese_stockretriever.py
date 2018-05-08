from stockretriever import (
    StockRetriever,
    QueryError,
)
from param import (
    RSS_CH_STOCK_SEARCH_URL,
    RSS_CH_NEWS_SEARCH_URL,
)
from urllib.parse import quote
import urllib.request
from bs4 import BeautifulSoup


def encoding_transform(data, enc='latin1', type_encode='strict', dec='big5'):
    try:
        data = str(data).encode(enc, type_encode).decode(dec)
    except UnicodeEncodeError as e:
        # print("encode error: {}, {}...", e, data[0:30])
        pass
    except UnicodeDecodeError as e:
        # print("decode error: {}, {}...", e, data[0:30])
        pass
    except UnicodeError as e:
        # print("unicode error: {}, {}...", e, data[0:30])
        pass
    return data


class ChineseStockRetriever(StockRetriever):
    def __init__(self):
        super(ChineseStockRetriever, self).__init__()

    def get_chinese_stock_news_feed(self, symbol):
        """ Retrieves the rss feed for the provided symbol. """

        feed_url = RSS_CH_STOCK_SEARCH_URL + symbol
        yql = "SELECT title, link, description, pubDate FROM rss " \
              "WHERE url=\'%s\'" % feed_url
        response = super(ChineseStockRetriever, self).execute(yql)
        result = response['query']['results']['item'][0]['title']
        if result.find('not found') > 0:
            raise QueryError('Feed for %s does not exist.' % symbol)
        else:
            return response['query']['results']['item']

    def get_all_chinese_important_news_feed(self):
        """ Retrieve the important news for the provided date """
        # we need to combine url first
        # result will like [url]1.html, [url]2.html ...
        _ = list()
        _.append(RSS_CH_NEWS_SEARCH_URL)
        SEARCH_FIELD_NUM = 5
        _ = _ * SEARCH_FIELD_NUM
        index_list = list(map(str, list(range(1, SEARCH_FIELD_NUM + 1))))
        _ = list(zip(_, index_list))
        feeds = [''.join(x) for x in _]
        feeds = ["\'" + x + ".html\'" for x in feeds]
        feeds = ",".join(feeds)

        yql = "SELECT * FROM rss WHERE url in (%s)" % feeds
        response = super(ChineseStockRetriever, self).execute(yql)
        result = response['query']['count']

        if result == 0:
            raise QueryError('Feed for %s does not exist.' % feeds)
        else:
            return response['query']['results']['item']

    def get_all_news(self, url):
        url = encoding_transform(url)
        url = quote(url, safe=":/")
        with urllib.request.urlopen(url) as f:
            html_doc = f.read()
            soup = BeautifulSoup(html_doc, 'html.parser')
            ret = soup.find_all('p')
            # change encode to BIG5
            ret = [encoding_transform(str(_.text), type_encode='ignore')
                   for _ in ret]
            return " ".join(ret)


# stocks = ChineseStockRetriever()
# r = stocks.get_all_chinese_important_news_feed()
# stocks.get_all_news(r[0]['link'])
