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
    
    def test_link_product_and_instruction(self):
        """Получение инструкции по guid"""

        products = self.api.get_products(start=0, count=1)
        i = self.api.get_instructions(products.data[0].guidInstruction)
        self.assertGreater(len(i.data), 0, "Instructions list is empty")

    
    def test_get_regions(self):
        must_be = ['vladimir', 'vologda', 'Moscowregion', 'barnaul']
        regions_response = self.api.get_regions()
        regions = regions_response.data.regions
        self.assertGreater(len(regions), 0, "Regions list is empty")
        region_codes = list(map(lambda r: r.CODE, regions))
        for require in must_be:
            self.assertIn(require, region_codes, f'Required word "{require}" not found')

    def test_get_categories(self):
        must_be = ['lekarstvennye-preparaty', 'bad', 'meditsinskie-izdeliya', 'medtekhnika', 'gigiena', 'kosmetika', 'sport-i-dieta']
        categories_response = self.api.get_categories()
        categories = categories_response.data.CATEGORIES
        self.assertGreater(len(categories), 0, "Categories list is empty")
        category_codes = list(map(lambda c: c.CODE, categories))
        for require in must_be:
            self.assertIn(require, category_codes, f'Required word "{require}" not found')


    
