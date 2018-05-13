from stockretriever import (
    StockRetriever,
    QueryError,
)
from param import (
    RSS_CH_STOCK_SEARCH_URL,
    RSS_CH_NEWS_SEARCH_URL,
)
from utils.encoding import encoding_transform
from urllib.parse import quote
import urllib.request
from bs4 import BeautifulSoup, Comment
import re


def article_filter(soup_ret_element):
    if re.match('<!--文章 start-->.*<!--文章 end-->',
                encoding_transform(str(soup_ret_element))):
        return True
    else:
        return False


def is_begin_tag(text):
    """Identify the start comment"""
    return (isinstance(text, Comment) and
            text.strip().startswith("文章 start"))


def is_end_tag(text):
    """Identify the end comment"""
    return (isinstance(text, Comment) and
            text.strip().startswith("文章 end"))


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
            result_list = response['query']['results']['item']
            finally_result_list = list()
            for r in result_list:
                _ = {k: encoding_transform(v) for k, v in r.items()}
                finally_result_list.append(_)
            return finally_result_list

    def get_all_news(self, url):
        url = encoding_transform(url)
        url = quote(url, safe=":/")
        with urllib.request.urlopen(url) as f:
            html_doc = f.read()
            soup = BeautifulSoup(html_doc, 'html.parser')

            result = ""
            for instance_begin_tag in soup.find_all(text=is_begin_tag):
                # We found a start comment, look at all text and comments:
                for text in instance_begin_tag.find_all_next(text=True):
                    text = encoding_transform(text)
                    if is_end_tag(text):
                        break
                    if isinstance(text, Comment):
                        continue
                    if not text.strip():
                        continue
                    result += text

            return result

# stocks = ChineseStockRetriever()
# r = stocks.get_all_chinese_important_news_feed()
# stocks.get_all_news(r[0]['link'])
