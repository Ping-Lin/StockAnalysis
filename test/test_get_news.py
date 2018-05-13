#! /usr/local/bin/python3
"""
.. moduleauthor:: Ping-Lin <billy3962@hotmail.com>
"""
from datetime import datetime
from stockretriever import QueryError
from modules.chinese_stockretriever import ChineseStockRetriever
from modules.db_wrapper import DBWrapper
from utils.print_error import print_error


def main():
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
                        if attr == "pubDate":
                            strtime = newsitems[attr]
                            fmt = '%a, %d %b %Y %X %Z'
                            datetime_obj = datetime.strptime(strtime, fmt)
                            timestamp = int(datetime_obj.timestamp())
                            values.append(timestamp)
                        else:
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


if __name__ == '__main__':
    main()
