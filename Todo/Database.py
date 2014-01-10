# Database access driver for ToDo app

from ConfigParser import ConfigParser
import psycopg2

class Database:
    def __init__(self):
        config = ConfigParser()
        config.read('attg0ra.cfg')
        self._conn = psycopg2.connect(
            "host='%s' dbname='%s' user='%s' password='%s'" % (
            config.get('db', 'hostname'),
            config.get('db', 'name'),
            config.get('db', 'username'),
            config.get('db', 'password')
        ))
        self._cur = self._conn.cursor()

    def __iter__(self):
        self._iter_cur = self._conn.cursor()
        cur = self._iter_cur
        cur.execute('select id, data from todo')
        return self

    def next(self):
        cur = self._iter_cur
        data = cur.fetchone()
        if data is not None:
            return data
        else:
            raise StopIteration

    def add_post(self, title, text):
        cur = self._cur
        cur.execute(
            'insert into todo (data) values (%s)', (text,)
        )
        self._conn.commit()

    def delete_post(self, id):
        cur = self._cur
        cur.execute(
            'delete from todo where id = %s', 
            (id,)
        )
        self._conn.commit()

    def update_post(self, id, data):
        cur = self._cur
        cur.execute(
            'update todo set data = %s where id = %s',
            (data, id, )
        )
        self._conn.commit()

    def is_post(self, id):
        cur = self._cur
        cur.execute(
            'select id from todo where id = %s',
            (id,)
        )
        if cur.fetchone() is not None:
            return True
        return False
