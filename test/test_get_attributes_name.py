#! /usr/local/bin/python3
"""
.. moduleauthor:: Ping-Lin <billy3962@hotmail.com>
"""

from modules.db_wrapper import DBWrapper
from utils.print_error import print_error


def example_of_get_table_attrs_list():
    with DBWrapper("news.db") as db:
        table_name = "yahoo_news"
        attrs_list = db.get_table_attrs_list(table_name)
        print(attrs_list)


def main():
    example_of_get_table_attrs_list()


if __name__ == '__main__':
    main()
