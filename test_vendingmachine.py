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

class Store(object):

    def __init__(self, name, price):
        self.name = name
        self.price = price



class VendorMachine(object):
    available_money = (10, 50, 100, 500, 1000)

    def __init__(self, number=5):
        self.money = 0
        self.products = {}

        for i in range(number):
            self.store(Store('cola', 120))

    def add_coin(self, coin):
        if coin not in self.available_money:
            return coin

        self.money += coin

    def show_price(self):
        return self.money

    def payback(self):
        payback = self.money
        self.money = 0

        return payback

    def store(self, drink):
        amount = 0
        if drink.name in self.products:
            amount += self.products[drink.name]['ammount']

        self.products.update({drink.name: {'price': drink.price, 'ammount': amount + 1}})

    def get_price(self, name):
        return self.products[name]['price']

    def get_ammount(self, name):
        return self.products[name]['ammount']




class TDDBCTest(TestCase):
    def setUp(self):
        self.vm = VendorMachine()
        self.money = self.vm.available_money

   # money = lambda: (10, 50, 100, 500, 1000)

   # @data_provider(money)
   # def test_foobar(self, money):
   #     """ 硬貨、紙幣を投入できる """
   #     self.assertEqual(self.vm.add_coin(money), 10)

    def test_add_(self):
        """ 硬貨、紙幣を投入できる """
        for m in self.money:
            self.assertEqual(self.vm.add_coin(m), None)

    def test_add_error(self):
        """ １円玉５円玉１万円を投入すると金額が返ってくる """
        fetal_money = (1, 5, 10000)
        for m in fetal_money:
            self.assertEqual(self.vm.add_coin(m), m)

    def test_add(self):
        """ 投入金額の総計を取得できる """
        self.vm.add_coin(10)
        self.vm.add_coin(50)
        self.assertEqual(self.vm.show_price(), 60)

    def test_payback(self):
        """ 払い戻しを行うと総計が返ってくる """
        self.vm.add_coin(10)
        self.vm.add_coin(500)
        self.assertEqual(self.vm.payback(), 510)
        self.assertEqual(self.vm.money, 0)

    def test_store(self):
        """ 名前と金額をセットする """
        store = Store('cola', 120)
        self.assertEqual(store.name,'cola')
        self.assertEqual(store.price, 120)

    def test_can_store_drink(self):
        """ ジュースを格納できる """
        expected = 120
        drink = Store('cola', expected)
        self.vm.store(drink)
        self.assertEqual(self.vm.get_price(drink.name), expected)

    def test_init_store(self):
        """ 初期状態でコーラを５本格納している """
        self.assertEqual(self.vm.get_ammount('cola'), 5)


