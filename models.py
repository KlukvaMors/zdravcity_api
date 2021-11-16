from pydantic import BaseModel, create_model, Field
from typing import Any, List, Optional
from decimal import Decimal

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
    guidEsId: str
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


class Price(BaseModel):
    xmlId: str = Field(description="Код товар")
    price: Decimal = Field(description="Протековская цена")
    priceOld: Optional[Decimal] = Field(description="Старая протековская цена")
    maxQuantity: Optional[int] = Field(description="Доступное количество")
    DATE_UPDATE: str
    spDiscountPrice: Optional[Any] = Field(description="Цена с учетом скидок SP")
    priceTypeId: str = Field(description="Недокументировано")
    itemGroup: Optional[List[int]]  = Field(description="Недокументировано")
    prDelivery: int = Field(description="Недокументировано")


class Search(BaseModel):
    XML_ID: str
    NAME: str
    MADE: str
    COUNTRY: str
    MNN: str
    RECIPE: bool
    PROPERTY_BESTSELLER_VALUE: Optional[str]
    PROPERTY_NOVELTY_VALUE: Optional[str]
    PROPERTY_RECIPE_VALUE: Optional[str]
    RATING: int
    PRICE_TYPE_ID: Optional[str]
    OLD_PRICE: Optional[str]
    PRICE: Optional[str]
    IMAGE: str
    IMAGE_BIG: str
    

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


class SubPriceResponse(BaseModel):
    items: List[Price]


class PriceResponse(BaseResponseModel):
    data: SubPriceResponse


class SubSearchResponse(BaseModel):
    items: List[Search]


class SearchResponse(BaseResponseModel):
    data: SubSearchResponse