# -*- coding: utf-8 -*-
from unittest import TestCase


def data_provider(fn_data_provider):
    """Data provider decorator, allows another callable to provide the data for the test"""
    def test_decorator(fn):
        def repl(self, *args):
            for i in fn_data_provider():
                try:
                    fn(self, *i)
                except AssertionError:
                    print "Assertion error caught with data set ", i
                    raise
        return repl
    return test_decorator


class VendorMachine(object):
    def __init__(self):
        self.money = 0
        pass

    def add_coin(self, coin):
        if coin == 30:
            return coin


        self.money += coin

    def show_price(self):
        return self.money


class TDDBCTest(TestCase):
    def setUp(self):
        self.vm = VendorMachine()


   # money = lambda: (10, 50, 100, 500, 1000)
    money = (10, 50, 100, 500, 1000)

   # @data_provider(money)
   # def test_foobar(self, money):
   #     """ 硬貨、紙幣を投入できる """
   #     self.assertEqual(self.vm.add_coin(money), 10)

    def test_add_(self):
        """ 硬貨、紙幣を投入できる """
        for m in self.money:
            self.assertEqual(self.vm.add_coin(m), None)







    def test_add_error(self):
        """ ３０円玉を投入すると金額が返ってくる """
        self.assertEqual(self.vm.add_coin(30), 30)




    def test_add(self):
        """ 投入金額の総計を取得できる """
        self.vm.add_coin(10)
        self.vm.add_coin(50)
        self.assertEqual(self.vm.show_price(), 60)

    def test_add_2(self):
        """ 投入金額の総計を取得できる """
        self.vm.add_coin(10)
        self.vm.add_coin(10)
        self.assertEqual(self.vm.show_price(), 20)




