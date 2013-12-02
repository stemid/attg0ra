# Database access driver for ToDo app

from ConfigParser import ConfigParser
import psycopg2

class Database:
    def __init__(self):
        config = ConfigParser()
        config.read('attg0ra.cfg')
        self._conn = psycopg2.connect(
            "host='%s' dbname='%s' user='%s' password='%s'" % (
            config.get('main', 'db_hostname'),
            config.get('main', 'db_name'),
            config.get('main', 'db_username'),
            config.get('main', 'db_password')
        ))
        self._cur = self._conn.cursor()

    def __iter__(self):
        self._iter_cur = self._conn.cursor()
        cur = self._iter_cur
        cur.execute('select edited, data from todo order by edited desc')
        return self

    def next(self):
        cur = self._iter_cur
        data = cur.fetchone()
        if data is not None:
            return data
        else:
            raise StopIteration

    def add_post(self, edited, title, text):
        cur = self._cur
        cur.execute(
            'insert into todo (data) values (%s)', (text,)
        )
        self._conn.commit()

    def delete_post(self, edited):
        cur = self._cur
        cur.execute(
            "delete from todo where edited = %s", 
            (edited,)
        )
        self._conn.commit()

    def update_post(self, edited, text):
        cur = self._cur
        cur.execute(
            "update todo set (edited = %s, data = %s) where edited = %s",
            (edited, text, )
        )
        self._conn.commit()

    def is_post(self, edited):
        cur = self._cur
        cur.execute(
            "select edited from todo where edited = %s",
            (edited,)
        )
        if cur.fetchone() is not None:
            return True
        return False
