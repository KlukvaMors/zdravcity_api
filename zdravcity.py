from typing import Dict, List, Type

import requests
from os import getenv
from pydantic import parse_obj_as

from models import CategoriesResponse, InstructionsResponse, ProductsResponse, RegionsResponse
from exceptions import  ApiException, HttpCodeException, API_EXCEPTIONS


class ZdravcityAPI:
    """
    Оболочка над API Zdravcity.ru
    """

    HOST = getenv("ZDRAVCITY_HOST", "https://zdravcity.ru")
    HOST_TEST = getenv("ZDRAVCITY_TEST_HOST", "https://bitrix-dev-cloud.zdravcity.ru")

    HEADERS_TEST = {
        'CF-Access-Client-Id': 'e270ececa4fbbb357bdfc6335b426189.access',
        'CF-Access-Client-Secret': '79b2de2d3e54f5509f5fbea515891293d0484b54309000096c170e9ec4362628',
        'Authorization': 'Basic bmV3X21vdXNlOjczNzM1MDA=',
    }

    HEADERS = {
        'Cookie': 'BITRIX_SM_ABTEST_s1=1%7CB; BITRIX_SM_OLD_FAVORITES_CHECKED=Y; PHPSESSID=2l1jo8ppfpk52b94c6cffkqmd9',
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
    }

    def __init__(self, token: str, test: bool = True):
        self.__token = token
        self.__test = test

    def __prepare_request(self, path: str, payload: Dict) -> requests.Response:
        headers = self.HEADERS.copy()
        if self.__test:
            headers.update(self.HEADERS_TEST)
        
        payload = {
            "token": self.__token,
            ** payload
        }

        host = self.HOST_TEST if self.__test else self.HOST

        return requests.post(f"{host}{path}", headers=headers, json=payload)

    def __check_http_code_ok(self, response: requests.Response):
        if 200 >= response.status_code < 300:
            return

        if 400 >= response.status_code < 600:
            raise HttpCodeException(f"Response status code: {response.status_code}")

        raise HttpCodeException("Unknown HTTP exception")

    def __check_error(self, json_payload):
        if not json_payload["status"]:
            return

        for exception in API_EXCEPTIONS:
            if json_payload['status'] == exception.STATUS:
                raise exception

        raise ApiException(json_payload["message"])

    def __api_method(self, path: str, return_type: Type, params: Dict = {}):
        response = self.__prepare_request(path, params)
        self.__check_http_code_ok(response)
        json_payload = response.json()
        self.__check_error(json_payload)
        return parse_obj_as(return_type, json_payload)

    def get_categories(self) -> CategoriesResponse:
        return self.__api_method("/api.client/getCategoryList/", CategoriesResponse)

    def get_products(self, start, count) -> ProductsResponse:
        return self.__api_method("/api.client/obtainEsEima/", ProductsResponse, {"start": start, "count":count})

    def get_regions(self) -> RegionsResponse:
        return self.__api_method("/api.client/getRegionList/", RegionsResponse)

    def get_instructions(self, start=0, count=1) -> InstructionsResponse:
        return self.__api_method("/api.client/obtainEsInstructionEima/", InstructionsResponse, {"start": start, "count": count})




if __name__ == "__main__":
    api = ZdravcityAPI("a3e68bab0ce536152ab9ea85ce8ecaac")
    result = api.get_instructions()
    print(result)