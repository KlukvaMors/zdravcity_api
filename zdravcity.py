from typing import Callable, Dict, List, Type
from os import getenv, path
from inspect import signature

import requests
from pydantic import parse_obj_as
from dotenv import load_dotenv

from models import CategoriesResponse, InstructionsResponse, PriceResponse, ProductsResponse, RegionsResponse
from exceptions import  ApiException, HttpCodeException, API_EXCEPTIONS

load_dotenv()


class ZdravcityAPI:
    """
    Оболочка над API Zdravcity.ru
    """

    def __init__(self, token: str, test: bool = True):
        self.__token = token
        self.__test = test
        self.__host = getenv("ZDRAVCITY_TEST_HOST") if test else getenv("ZDRAVCITY_HOST")

        self.__headers = {
            'Cookie': 'BITRIX_SM_ABTEST_s1=1%7CB; BITRIX_SM_OLD_FAVORITES_CHECKED=Y; PHPSESSID=2l1jo8ppfpk52b94c6cffkqmd9',
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
        }
        if test:
            self.__headers.update({
                'CF-Access-Client-Id': getenv('ZDRAVCITY_CF_Access_Client_Id'),
                'CF-Access-Client-Secret': getenv('ZDRAVCITY_CF_Access_Client_Secret'),
                'Authorization': getenv('ZDRAVCITY_Authorization'),
            })

    def __api_method(self, path: str, return_type: Type, params: Dict = {}):
        payload =  dict(token=self.__token)
        payload.update(params)
        
        response = requests.post(f"{self.__host}{path}", headers=self.__headers, json=payload)

        if not (200 >= response.status_code < 300):
            raise HttpCodeException(f"Response status code: {response.status_code}")

        json_response = response.json()

        if json_response['status'] != 0:
            for exception in API_EXCEPTIONS:
                if json_response['status'] == exception.STATUS:
                    raise exception

        
        return parse_obj_as(return_type, json_response)


    def get_categories(self) -> CategoriesResponse:
        return self.__api_method("/api.client/getCategoryList/", CategoriesResponse)


    def get_products(self, start: int=0, count: int=1) -> ProductsResponse:
        return self.__api_method(
            path="/api.client/obtainEsEima/",
            return_type=ProductsResponse,
            params={'start': start, 'count': count}
        )

    def get_regions(self) -> RegionsResponse:
        return self.__api_method("/api.client/getRegionList/", RegionsResponse)

    def get_instructions(self, guid: str, start: int=0, count: int=1) -> InstructionsResponse:
        return self.__api_method(
            path="/api.client/obtainEsInstructionEima/",
            return_type=InstructionsResponse,
            params={'guidInstruction': guid, 'start': start, 'count': count}
        )

    def get_prices(self, region_code: str, categories: List[str]) -> PriceResponse:
        """Получение цен и остатков по активным позициям из справочника товара """
        return self.__api_method(
            path="/api.client/getPrices/",
            return_type=PriceResponse,
            params={"region_code": region_code, "show": categories}
        )


if __name__ == "__main__":
    api = ZdravcityAPI(getenv("ZDRAVCITY_TOKEN"))
    result = api.get_products()
    print(result)
    # prices_response = api.get_prices(region_code="vladimir", categories=["igly-i-shpritsy"])
    # length_response = len(prices_response.data.items)
    # print(length_response)
    # 