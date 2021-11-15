from unittest import TestCase
from zdravcity import ZdravcityAPI
from os import getenv

class TestZdravcityAPI(TestCase):

    def setUp(self):
        self.api = ZdravcityAPI(token=getenv("ZDRAVCITY_TOKEN"), test=True)

    
    def test_1(self):
        products = self.api.get_products(start=0, count=1)