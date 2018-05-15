#! /usr/local/bin/python3
"""
.. moduleauthor:: Ping-Lin <billy3962@hotmail.com>
"""

from modules.db_wrapper import DBWrapper
from utils.print_error import print_error


def example_of_get_data_by_time():
    with DBWrapper("news.db") as db:
        table_name = "yahoo_news"
        start = "1526196605"
        end = "1526197778"
        try:
            # exmple of get data by time
            data_list = db.get_data_by_time(table_name, start, end)
            for data in data_list:
                # check index
                print(data[0])
        except Exception as e:
            print_error(e, "get data fail")


def example_of_get_count_query_by_time():
    with DBWrapper("news.db") as db:
        table_name = "yahoo_news"
        start = "1526196605"
        end = "1526197778"
        try:
            # exmple of get data by time and return count of query string
            query_list = ["金融", "觀察"]
            count = db.get_count_query_by_time(
                        table_name,
                        query_list,
                        start,
                        end,
                        query_col="title"   # default is allnews
                    )
            print("count of {}: {}".format(query_list, count))
        except Exception as e:
            print_error(e, "get data fail")


def main():
    example_of_get_data_by_time()
    print("\n============================\n")
    example_of_get_count_query_by_time()


if __name__ == '__main__':
    main()
