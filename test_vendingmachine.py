# -*- coding: utf-8 -*-
from unittest import TestCase

class VendorMachine(object):
    def __init__(self):
        self.money = 0
        pass

    def add_coin(self, coin):
        self.money += coin

    def show_price(self):
        return self.money


class TDDBCTest(TestCase):
    def setUp(self):
        self.vm = VendorMachine()

    def test_add_10(self):
        """ 10 円玉を投入できる """
        self.assertEqual(self.vm.add_coin(10), None)

    #def test_add_error(self):
    #    """ ３０円玉を投入すると金額が返ってくる """
    #    self.assertEqual(self.vm.add_coin(30), 30)

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




