# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'


from spider.extension.generators import TableParser
from spider.framework.storage import HBaseData
from public.utils import tables, tools


class MoneyFlow(HBaseData):
    """
    money flow
    """
    def __init__(self, code, name, price, amplitude, exchange, flow_in, flow_out, balance, trade_amount, ratio, big_flow_in):

        self.code = code
        self.name = name
        self.price = price
        self.amplitude = amplitude
        self.exchange = exchange
        self.flow_in = flow_in
        self.flow_out = flow_out
        self.balance = balance
        self.trade_amount = trade_amount
        self.ratio = ratio
        self.big_flow_in = big_flow_in

    def table(self):
        return tables.TABLE_SHARE_MONEY

    def row(self):

        return tables.ROW_ID.format(self.code, tools.current_date())

    def columns(self):

        return {
            tables.COLUMN_FAMILY: {
                tables.CODE: self.code,
                tables.NAME: self.name,
                tables.PRICE: self.price,
                tables.AMPLITUDE: self.amplitude,
                tables.EXCHANGE: self.exchange,
                tables.FLOW_IN: self.flow_in,
                tables.FLOW_OUT: self.flow_out,
                tables.BALANCE: self.balance,
                tables.TRADE_AMOUNT: self.trade_amount,
                tables.RATIO: self.ratio,
                tables.BIG_FLOW_IN: self.big_flow_in
            }
        }


class MoneyFlowParser(TableParser):

    def parse_item(self, tds):

        return MoneyFlow(
            self.parse_tag_a(tds[1])[0],
            self.parse_tag_a(tds[2])[0],
            tds[3].string,
            tds[4].string,
            tds[5].string,
            tds[6].string,
            tds[7].string,
            tds[8].string,
            tds[9].string,
            tds[10].string,
            tds[11].string,
        )