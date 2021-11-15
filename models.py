from pydantic import BaseModel, create_model
from typing import List, Optional


class SubCategory(BaseModel):
    ID: Optional[str] 
    NAME: str
    CODE: str


class Category(BaseModel):
    ID: Optional[str] 
    NAME: str
    CODE: str
    SUBCATEGORIES: List[SubCategory]


class Product(BaseModel):
    itemName: str
    itemShortDesc: Optional[str]
    producerName: str
    storingCondition: Optional[str]
    producerCountry: str
    guidInstruction: str


class Region(BaseModel):
    NAME: str
    REAL_NAME: str
    CODE: str
    REGION: str
    LAT: Optional[str]
    LONG: Optional[str]


class Instruction(BaseModel):
    guidInstruction: str
    indication: str
    contraIndication: str
    specialInstruction: str
    pharmAction: str
    dosage: str
    interaction: str
    overDosage: str
    sideEffect: str
    rowTs: int


# RESPONSE MODELS


class BaseResponseModel(BaseModel):
    status: str
    message: str


class ProductsResponse(BaseResponseModel):
    data: List[Product]


class SubCategoriesResponse(BaseModel):
    CATEGORIES: List[Category]


class CategoriesResponse(BaseResponseModel):
    data: SubCategoriesResponse


class SubRegionsResponse(BaseModel):
    regions: List[Region]


class RegionsResponse(BaseResponseModel):
    data: SubRegionsResponse


class InstructionsResponse(BaseResponseModel):
    data: List[Instruction]