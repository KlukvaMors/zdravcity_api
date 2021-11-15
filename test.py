from unittest import TestCase
from zdravcity import ZdravcityAPI
from exceptions import IncorrectTokenException
from os import getenv

class TestZdravcityAPI(TestCase):

    def setUp(self):
        self.api = ZdravcityAPI(token=getenv("ZDRAVCITY_TOKEN"), test=True)
        self.bad_api = ZdravcityAPI(token="foobuzz", test=True)


    def test_exception_token(self):
        """Проверка поднятия исключения при некоррктном токене"""

        with self.assertRaises(IncorrectTokenException):
            self.bad_api.get_products()

    def test_get_prices(self):
        
        prices_response = self.api.get_prices(region_code="vladimir", categories=["igly-i-shpritsy"])
        length_response = len(prices_response.data.items)
        print(length_response)
        self.assertGreater(length_response, 0)
    
    def test_1(self):
        """Получение инструкции по guid"""

        products = self.api.get_products(start=0, count=1)
        i = self.api.get_instructions(products.data[0].guidInstruction)
        self.assertGreater(len(i.data), 0, "Instruction not found")

    
