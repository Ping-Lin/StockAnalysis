#! /usr/local/bin/python3
"""
.. module:: db_wrapper
    :synopsis: a class for sqlite db wrapper operations

.. moduleauthor:: Ping-Lin <billy3962@hotmail.com>
"""
import sqlite3
import inspect
import hashlib
import logging


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

        logging.error("sqlite3 error occurred: {}\
                       \nFile: \"{}\", line: {}, in {}\n".format(
                       e.args[0], info.filename, info.lineno, info.function))

    def create_table(self, table_name, attr_list):
        """
        create table name with attr_list

        :Args:
            |  table_name (string): table name
            |  attr_list (list): table header

        >>> with DBWrapper() as db:
        ...     table_name = "yahoo_news"
        ...     attr_list = ["description", "contents"]
        ...     db.create_table(table_name, attr_list)

        this will create table name "yahoo_news" and
        column ["id", "description", "contents"]
        """
        attr_list = ["id PRIMARY KEY"] + attr_list
        str_attr = ",".join(attr_list)
        try:
            sql = '''CREATE TABLE IF NOT EXISTS {} ({})'''.format(
                    table_name, str_attr)
            self._cursor.execute(sql)
        except sqlite3.Error as e:
            self._print_error(e)

    def _get_hash(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def data_insert(self, table_name, attr_list, values_list):
        """
        |  insert data into table_name with attr_list and values_list
        |  auto add primary key (id), default gen from first value of attributes
        |  (gen method: hashlib.md5)

        :Args:
            |  table_name (string): table name
            |  attr_list (list): table header
            |  values_list (list): list of values list you want to insert

        >>> with DBWrapper() as db:
        ...     table_name = "yahoo_news"
        ...     attr_list = ["title", "description"]
        ...     values_list = [["Hello", "hello world"],
        ...                    ["Marry", "Marry me"]]
        ...     db.data_insert(table_name, attr_list, values_list)

        |  this will add data into "yahoo_news" table
        |  ["8b1a9953c4611296a827abf8c47804d7", "Hello", "hello world"]
        |  ["fd50a6e193cab17e500275acb1c0a4aa", "Marry", "Marry me"]

        (ie: first value is gen from hashlib.md5("Hello"))
        """
        for i in range(len(values_list)):
            primary_key = self._get_hash(values_list[i][0])
            values_list[i] = [primary_key] + values_list[i]

        attr_list = ["id"] + attr_list
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

    def data_update_time(self, table_name, new_value, idname):
        """
        One use function

        >>> from datetime import datetime
        ...     with DBWrapper("news.db") as db:
        ...         table_name = "yahoo_news"
        ...         attr_list = ["id", "pubDate"]
        ...         data_list = db.get_data_from_attr(table_name, attr_list)
        ...         for item in data_list:
        ...             idname = item[0]
        ...             strtime = item[1]
        ...             datetime_object = datetime.strptime(strtime,
                                                            '%a, %d %b %Y %X %Z')
        ...             print(idname, strtime, datetime_object.timestamp())
        ...             db.data_update_time(table_name,
                                            int(datetime_object.timestamp()),
                                            idname)
        ...         print(len(data_list))

        """
        try:
            task = (new_value, idname)
            sql = "UPDATE yahoo_news SET pubDate = ? WHERE id = ?"
            self._cursor.execute(sql, task)
        except sqlite3.Error as e:
            self._print_error(e)

    def get_table_attrs_list(self, table_name):
        """
        get attribute header list

        :Args:
            |  table_name (string): table name

        :Returns:
            |  a list of table attrs

        >>> with DBWrapper() as db:
        ...     table_name = "yahoo_news"
        ...     db.get_table_attrs_list(table_name)
        >>>     ['id', 'title', 'description', 'link', 'pubDate', 'allNews']
        """
        try:
            sql = "SELECT * FROM {}".format(table_name)
            self._cursor.execute(sql)
            attrs_list = [d[0] for d in self._cursor.description]
            return attrs_list
        except sqlite3.Error as e:
            self._print_error(e)

    def get_data_from_attr(self, table_name, attr_list):
        """
        get data from specific attrs list

        |  *** FIXME ***
        |  now get all the data in the memory, because datas are small now

        :Args:
            |  table_name (string): table name
            |  attr_list (list): table header

        :Returns:
            |  a list of data list

        >>> with DBWrapper() as db:
        ...     table_name = "yahoo_news"
        ...     attr_list = db.get_table_attrs_list(table_name)
        ...     data_list = db.get_data_from_attr(table_name, attr_list)
        >>>[["xxxx", "yyyy", ...], [...]]
        """
        str_attr = ",".join(attr_list)
        try:
            sql = "SELECT {} FROM {}".format(
                   str_attr, table_name)
            self._cursor.execute(sql)
            data_list = list()
            for row in self._cursor:
                data_list.append(list(row))

            return data_list
        except sqlite3.Error as e:
            self._print_error(e)

    def get_data_by_time(self, table_name, start, end, attr="pubDate"):
        """
        |  get data from all attrs from start time to end time
        |  This is a wrapper function for easy using

        |  *** FIXME ***
        |  1. change to get attr list not 'select *'
        |  2. now get all the data in the memory, because datas are small now
            here can change future

        eg: SELECT * from yahoo_news where pubDate > 1526196605

        :Args:
            |  table_name (string): table name
            |  start (*): compare value, eg: unix time stamp
            |  end (*): compare value, eg: unix time stamp

        :Kwargs:
            |  attr (string): column you want to compare between start and end,
                default -> "pubDate"

        :Returns:
            |  a list of data list

        >>> with DBWrapper() as db:
        ...     table_name = "yahoo_news"
        ...     start = "1526196605"
        ...     end = "1526197778"
        ...     data_list = db.get_data_by_time(table_name, start, end)
        """

        try:
            sql = "SELECT * from {} where {} >= {} and {} < {}".format(
                   table_name, attr, start, attr, end)
            self._cursor.execute(sql)
            data_list = list()
            for row in self._cursor:
                data_list.append(list(row))
                logging.debug(list(row))
            return data_list
        except sqlite3.Error as e:
            self._print_error(e)

    def get_count_query_by_time(self,
                                table_name,
                                query_list,
                                start,
                                end,
                                attr="pubDate",
                                query_col="allnews"):
        """
        |  get count of appearance from query list, this will call
           get_data_by_time()

        This is a wrapper function for easy using

        :Args:
            |  table_name (string): table name
            |  query_list (list): list of query words
            |  start (): compare value, eg: unix time stamp
            |  end (): compare value, eg: unix time stamp

        :Kwargs:
            |  attr (string): column you want to compare between start and end
                , default: "pubDate"
            |  query_col (string): can be "all", "title", "desc" or "allnews"
                , default: "allnews"

        :Returns:
            |  a number of count

        >>> with DBWrapper() as db:
        ...     table_name = "yahoo_news"
        ...     query_list = ["金融", "觀察"]
        ...     start = "1526196605"
        ...     end = "1526197778"
        ...     count = db.get_count_query_by_time(
        ...                    table_name,
        ...                    query_list,
        ...                    start,
        ...                    end,
        ...                    query_col="title"   # default is allnews
        ...             )
        """
        data_list = self.get_data_by_time(table_name, start, end, attr)

        def get_attr_list(query_col_string):
            # map to database col number
            array_num_list = list()
            if "all" == query_col_string.lower():
                array_num_list = [1, 2, 5] + array_num_list
            else:
                if "title" in query_col_string.lower():
                    array_num_list.append(1)
                if "desc" in query_col_string.lower():
                    array_num_list.append(2)
                if "allnews" in query_col_string.lower():
                    array_num_list.append(5)
            return array_num_list

        count = 0
        for data in data_list:
            wanted_col = [data[i] for i in get_attr_list(query_col)]
            for _ in wanted_col:
                logging.debug(_)
                logging.debug("-----------")
                for q in query_list:
                    count += str(_).count(q)
        return count
