"""
This is test module for unit test in django

"""

from app import calc
from django.test import SimpleTestCase


class TestAddFunc(SimpleTestCase):

    def tester_adding(self):
        
        res = calc.func_add(4, 5)
        self.assertEqual(res, 9)

    def tester_subtracting(self):

        res = calc.func_subtract(5, 5)
        self.assertEqual(res, 0)