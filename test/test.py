from stockretriever import QueryError
from modules.chinese_stockretriever import ChineseStockRetriever
from modules.db_wrapper import DBWrapper
import inspect


def print_error(e, error_string):
    # 0 represents this line
    # 1 represents line at caller
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)

    print("{}: {}\nFile: \"{}\", line: {}, in {}"
          .format(error_string, e, info.filename, info.lineno, info.function))


stocks = ChineseStockRetriever()

with DBWrapper("news.db") as db:
    table_name = "yahoo_news"
    attr_list = ["title", "description", "link", "pubDate", "allNews"]
    db.create_table(table_name, attr_list)
    try:
        '''
        gets news articles related to symbol, returns a dictionary,
        it have printed title and description below in the for loop
        the dictionary has the following fields:
        title, link, description, pubDate
        '''
        news = stocks.get_all_chinese_important_news_feed()
        values_list = list()

        for newsitems in news:
            values = list()
            for attr in attr_list[0: -1]:
                if newsitems[attr]:
                    values.append(newsitems[attr])
                else:
                    break
            else:
                # if every data get, add into db
                try:
                    values.append(stocks.get_all_news(newsitems['link']))
                except Exception as e:
                    print_error(e, "get all news fail")
                    continue
                values_list.append(values)

        db.insert_data(table_name, attr_list, values_list)
    except QueryError as e:
        print('couldnt get yahoo feed.\nreason: %s' % e)
