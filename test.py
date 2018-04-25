from chinese_stockretriever import ChineseStockRetriever
from stockretriever import QueryError

stocks = ChineseStockRetriever()

symbols = "2017+%E9%B4%BB%E6%B5%B7?ei=UTF-8"

try:
    '''
    gets news articles related to symbol, returns a dictionary,
    it have printed title and description below in the for loop
    the dictionary has the following fields: title, link, description, pubDate
    '''
    news = stocks.get_chinese_news_feed(symbols)
    for newsitems in news:
        title = ''
        desc = ''
        if newsitems['title']:
            print('TITLE: ', newsitems['title'])
            title = newsitems['title'] + ' '
        else:
            title = ''

        if newsitems['description']:
            print('DESCRP: ', newsitems['description'])
            desc = newsitems['description']
except QueryError as e:
    print('couldnt get yahoo feed.\nreason: %s' % e)
