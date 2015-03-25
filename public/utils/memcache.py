# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
TRADE_TIME = 'trade_time'
STOCK_CODE = 'stock_code'
__author__ = 'keping.chu'
import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
memcache = redis.Redis(connection_pool=pool)
visited = "visited"
unvisited = "unvisited"


def is_table_collected(table_name):

    return memcache.exists(table_name)


def table_collected(table_name):
    memcache.setex(table_name, 1, 3600*12)


def set_visited():

    memcache.set(visited, visited)


def set_unvisited():

    memcache.set(visited, unvisited)


def get_visited():

    ret_value = memcache.get(visited)
    if ret_value is None:
        set_visited()

    return memcache.get(visited)


def set_reverse():

    if get_visited() == visited:
        set_unvisited()
    else:
        set_visited()


def get_big_bill():

    code = memcache.get(STOCK_CODE)

    time = memcache.get(TRADE_TIME)

    return code, time


def set_big_bill(code, time):

    memcache.set(STOCK_CODE, code)
    memcache.set(TRADE_TIME, time)

