# -*- coding: utf-8 -*-
"""
    TDD Bootcamp Osaka
    ~~~~~~~~~~~~~~~~~~

    Python unittest.


    :copyright: (c) 2012 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from unittest import TestCase
from functools import wraps


def paramterized(**kwargs):
    def _paramterized_test(func):
        @wraps(func)
        def __paramterized_test(*args):
            func(args[0], kwargs)
            return func
        return __paramterized_test
    return _paramterized_test


class Drink(object):
    def __init__(self, name, price):
        self.name = name
        self.price = price


class VendorMachine(object):
    available_money = (10, 50, 100, 500, 1000)
    default_amount = 5

    def __init__(self):
        self.money = 0
        self.products = {}

        for i in range(self.default_amount):
            self.store(Drink('cola', 120))


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
            amount += self.products[drink.name]['amount']

        self.products.update({
            drink.name: {'price': drink.price, 'amount': amount + 1}}
        )

    def get_price(self, name):
        return self.products[name]['price']

    def get_amount(self, name):
        return self.products[name]['amount']


class TestVendingMachine(TestCase):
    def setUp(self):
        self.vm = VendorMachine()
        self.money = self.vm.available_money

    @paramterized(param=10, expected=None)
    @paramterized(param=50, expected=None)
    @paramterized(param=100, expected=None)
    @paramterized(param=500, expected=None)
    @paramterized(param=1000, expected=None)
    def test_paramterize1d(self, params):
        """ 硬貨、紙幣を投入できる """
        self.assertEqual(self.vm.add_coin(params['param']), params['expected'])

    @paramterized(param=1, expected=1)
    @paramterized(param=5, expected=5)
    @paramterized(param=10000, expected=10000)
    def test_paramterized_error(self, params):
        """ １円玉５円玉１万円を投入すると金額が返ってくる """
        self.assertEqual(self.vm.add_coin(params['param']), params['expected'])

    def test_show_total_price(self):
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
        store = Drink('cola', 120)
        self.assertEqual(store.name,'cola')
        self.assertEqual(store.price, 120)

    def test_can_store_drink(self):
        """ ジュースを格納できる """
        expected = 120
        drink = Drink('cola', expected)
        self.vm.store(drink)
        self.assertEqual(self.vm.get_price(drink.name), expected)

    def test_init_store(self):
        """ 初期状態でコーラを５本格納している """
        expected = self.vm.default_amount
        self.assertEqual(self.vm.get_amount('cola'), expected)

    def test_add_cola(self):
        """ コーラを一本自販機に追加する """
        self.vm.store(Drink('cola', 120))
        self.assertEqual(self.vm.get_amount('cola'), 6)

    def test_add_another_drink(self):
        """ コーラ以外のドリンクを格納して情報を取得できる """
        drink = Drink('orange', 100)
        self.vm.store(drink)
        self.assertEqual(self.vm.get_amount('orange'), 1)
        self.assertEqual(self.vm.get_amount('cola'), self.vm.default_amount)

