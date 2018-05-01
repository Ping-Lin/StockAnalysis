#! /usr/local/bin/python3
"""
.. module:: db_wrapper
    :synopsis: a class for sqlite db wrapper operations

.. moduleauthor:: Ping-Lin <billy3962@hotmail.com>
"""
import sqlite3


class DBWrapper(object):
    """
        DB wrapper class for easily operating db
    """
    def __init__(self):
        self._conn = sqlite3.connect('news.db')
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self):
        self.commit()
        self._conn.close()

    def commit(self):
        self._conn.commit()

    def create_table(self, title, header_list):
        """
        Args:
            title (string): table name
            header_list (list): table header

        >>> with DBWrapper as db:
        ...     title = "news"
        ...     header_list = ["description", "contents"]
        ...     db.create_table(title, header_list)
        """
        str_header = header_list.join(',')
        sql = '''CREATE TABLE ? ?''', (title, str_header)
        self._conn.execute(sql)


def main():
    pass


if __name__ == '__main__':
    main()
