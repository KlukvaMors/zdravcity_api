from unittest import TestCase
from zdravcity import ZdravcityAPI
from os import getenv

class TestZdravcityAPI(TestCase):

    def setUp(self):
        self.api = ZdravcityAPI(token=getenv("ZDRAVCITY_TOKEN"), test=True)

    
    def test_1(self):
        """Получение инструкции по guid"""

        products = self.api.get_products(start=0, count=1)
        i = self.api.get_instructions(products.data[0].guidInstruction)
        self.assertGreater(len(i.data), 0, "Instruction not found")

    