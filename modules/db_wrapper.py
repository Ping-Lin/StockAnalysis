#! /usr/local/bin/python3
"""
.. module:: db_wrapper
    :synopsis: a class for sqlite db wrapper operations

.. moduleauthor:: Ping-Lin <billy3962@hotmail.com>
"""
import sqlite3
import inspect
import hashlib


class DBWrapper(object):
    """
        DB wrapper class for easily operating db
    """
    def __init__(self, db_name):
        self._conn = sqlite3.connect(db_name)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_ty, exc_val, tb):
        self._commit()
        self._close()

    def _commit(self):
        self._conn.commit()

    def _close(self):
        self._conn.close()

    def _print_error(self, e):
        # 0 represents this line
        # 1 represents line at caller
        callerframerecord = inspect.stack()[1]
        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)

        print("sqlite3 error occurred: {}\nFile: \"{}\", line: {}, in {}"
              .format(e.args[0], info.filename, info.lineno, info.function))

    def create_table(self, table_name, attr_list):
        """
        Args:
            table_name (string): table name
            pk (string): primary key, use title and md5 hash
            attr_list (list): table header

        >>> with DBWrapper() as db:
        ...     table_name = "yahoo_news"
        ...     attr_list = ["description", "contents"]
        ...     db.create_table(table_name, attr_list)
        """
        attr_list = ["id PRIMARY KEY"] + attr_list
        str_attr = ",".join(attr_list)
        try:
            sql = '''CREATE TABLE {} ({})'''.format(
                    table_name, str_attr)
            self._cursor.execute(sql)
        except sqlite3.Error as e:
            self._print_error(e)

    def _get_hash(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def insert_data(self, table_name, attr_list, values_list):
        """
        """
        for i in range(len(values_list)):
            primary_key = self._get_hash(values_list[i][0])
            values_list[i] = [primary_key] + values_list[i]

        str_attr = ",".join(attr_list)
        try:
            sql = "INSERT OR IGNORE INTO {} ({}) VALUES".format(
                    table_name, str_attr)
            # use ? for placeholder, num = len(attr_list)
            tmp_str = ",".join(["?"] * len(attr_list))
            sql += " ({})".format(tmp_str)
            self._cursor.executemany(sql, values_list)
        except sqlite3.Error as e:
            self._print_error(e)

    def get_data_from_name(self, table_name, attr_list, name):
        str_attr = ",".join(attr_list)
        try:
            sql = "SELECT {} from {}".format(str_attr, table_name)
            self._cursor.execute(sql)
            data_list = list()
            for row in self._cursor:
                data_list.append(row)

            return data_list
        except sqlite3.Error as e:
            self._print_error(e)
