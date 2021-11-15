from typing import Dict, List, Type

import requests
from os import getenv
from pydantic import parse_obj_as
from dotenv import load_dotenv

from models import CategoriesResponse, InstructionsResponse, ProductsResponse, RegionsResponse
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


    def __send_request(self, path: str, payload: Dict) -> requests.Response:

        payload = {
            "token": self.__token,
            ** payload
        }

        return requests.post(f"{self.__host}{path}", headers=self.__headers, json=payload)

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
        response = self.__send_request(path, params)
        self.__check_http_code_ok(response)
        json_payload = response.json()
        self.__check_error(json_payload)
        return parse_obj_as(return_type, json_payload)

    def get_categories(self) -> CategoriesResponse:
        return self.__api_method("/api.client/getCategoryList/", CategoriesResponse)

    def get_products(self, start=0, count=1) -> ProductsResponse:
        return self.__api_method("/api.client/obtainEsEima/", ProductsResponse, {"start": start, "count":count})

    def get_regions(self) -> RegionsResponse:
        return self.__api_method("/api.client/getRegionList/", RegionsResponse)

    def get_instructions(self, guid: str, start=0, count=1) -> InstructionsResponse:
        return self.__api_method(
            path="/api.client/obtainEsInstructionEima/",
            return_type=InstructionsResponse,
            params={"start": start, "count": count, "guidInstruction": guid})




if __name__ == "__main__":
    api = ZdravcityAPI(getenv("ZDRAVCITY_TOKEN"))
    result = api.get_instructions()
    print(result)