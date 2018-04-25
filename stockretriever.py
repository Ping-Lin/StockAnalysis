import sys
from param import (
    PUBLIC_API_URL,
    DATATABLES_URL,
    HISTORICAL_URL,
    RSS_URL,
    FINANCE_TABLES)
import urllib
import http.client

try:
    import simplejson as json
except ImportError:
    import json


class YQLQuery(object):
    def __init__(self):
        self.connection = http.client.HTTPConnection('query.yahooapis.com')

    def execute(self, yql):
        queryString = urllib.parse.urlencode({'q': yql,
                                              'format': 'json',
                                              'env': DATATABLES_URL})
        self.connection.request('GET', PUBLIC_API_URL + '?' + queryString)
        response_text = self.connection.getresponse().read().decode('UTF-8')
        return json.loads(response_text)


class QueryError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class StockRetriever(YQLQuery):
    """A wrapper for the Yahoo! Finance YQL api."""

    def __init__(self):
        super(StockRetriever, self).__init__()

    def __format_symbol_list(self, symbolList):
        return ",".join(["\""+stock+"\"" for stock in symbolList])

    def __is_valid_response(self, response, field):
        return 'query' in response and 'results' in response['query'] \
                and field in response['query']['results']

    def __validate_response(self, response, tagToCheck):
        if self.__is_valid_response(response, tagToCheck):
            quoteInfo = response['query']['results'][tagToCheck]
        else:
            if 'error' in response:
                raise QueryError('YQL query failed with error: "%s".'
                                 % response['error']['description'])
            else:
                raise QueryError('YQL response malformed.')
        return quoteInfo

    def get_current_info(self, symbolList, columnsToRetrieve='*'):
        """Retrieves the latest data (15 minute delay) for the
        provided symbols."""

        columns = ','.join(columnsToRetrieve)
        symbols = self.__format_symbol_list(symbolList)

        yql = 'select %s from %s where symbol in (%s)' \
              % (columns, FINANCE_TABLES['quotes'], symbols)
        response = super(StockRetriever, self).execute(yql)
        return self.__validate_response(response, 'quote')

    def get_historical_info(self, symbol):
        """Retrieves historical stock data for the provided symbol.
        Historical data includes date, open, close, high, low, volume,
        and adjusted close."""

        yql = 'select * from csv where url=\'%s\'' \
              ' and columns=\"Date,Open,High,Low,Close,Volume,AdjClose\"' \
              % (HISTORICAL_URL + symbol)
        results = super(StockRetriever, self).execute(yql)
        # delete first row which contains column names
        del results['query']['results']['row'][0]
        return results['query']['results']['row']

    def get_news_feed(self, symbol):
        """Retrieves the rss feed for the provided symbol."""

        feedUrl = RSS_URL + symbol
        yql = 'select title, link, description, pubDate from rss ' \
              'where url=\'%s\'' % feedUrl
        response = super(StockRetriever, self).execute(yql)
        result = response['query']['results']['item'][0]['title']
        if result.find('not found') > 0:
            raise QueryError('Feed for %s does not exist.' % symbol)
        else:
            return response['query']['results']['item']

    def get_options_info(self, symbol, expiration='', columnsToRetrieve='*'):
        """Retrieves options data for the provided symbol."""

        columns = ','.join(columnsToRetrieve)
        yql = 'select %s from %s where symbol = \'%s\'' \
              % (columns, FINANCE_TABLES['options'], symbol)

        if expiration != '':
            yql += " and expiration='%s'" % (expiration)

        response = super(StockRetriever, self).execute(yql)
        return self.__validate_response(response, 'optionsChain')

    def get_index_summary(self, index, columnsToRetrieve='*'):
        columns = ','.join(columnsToRetrieve)
        yql = 'select %s from %s where symbol = \'@%s\'' \
              % (columns, FINANCE_TABLES['quoteslist'], index)
        response = super(StockRetriever, self).execute(yql)
        return self.__validate_response(response, 'quote')

    def get_industry_ids(self):
        """retrieves all industry names and ids."""

        yql = 'select * from %s' % FINANCE_TABLES['sectors']
        response = super(StockRetriever, self).execute(yql)
        return self.__validate_response(response, 'sector')

    def get_industry_index(self, id):
        """retrieves all symbols that belong to an industry."""

        yql = 'select * from %s where id =\'%s\'' \
              % (FINANCE_TABLES['industry'], id)
        response = super(StockRetriever, self).execute(yql)
        return self.__validate_response(response, 'industry')


if __name__ == "__main__":
    retriever = StockRetriever()
    try:
        retriever.get_current_info(sys.argv[1:])
        # print(retriever.get_industry_ids())
        # print(retriever.get_news_feed('yhoo'))
    except QueryError as e:
        # print(e)
        # self.response.write('<p>%s</p>' % e)
        sys.exit(2)
