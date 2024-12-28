from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse,PlainTextResponse
from pydantic import BaseModel,field_validator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any,Iterable,Union
import pytest
from models.model import Products
from database.db import get_db
from .import ResourceState

router=APIRouter()

# List all products 

@router.get("/")
async def list_products(db:AsyncSession=Depends(get_db)):
    all_products=await get_all_products(db)
    if all_products==None:
        return PlainTextResponse(status_code=500,content="Internal Server Error")
    product_data=[]
    for product in all_products:
        cur_product=product.to_dictionary()
        product_data.append(cur_product)
    return JSONResponse(status_code=200,content={"product_count":len(product_data),"products":product_data})

async def get_all_products(db:AsyncSession)->Union[Iterable[Products],None]:
    try:
        products_query_result= await db.execute(select(Products))
        products=products_query_result.scalars().all()
        return products
    except:
        return None

# Insert a new Product

class ProductBody(BaseModel):
    name:str
    description:str
    price:float
    stock:int=1

    @field_validator("name")
    @classmethod
    def ensure_name_non_empty(cls,name:Any):
        if len(name)==0:
            raise ValueError("Product name must be non-empty.")
        if len(name)>100:
            raise ValueError("Product name length must be smaller than 100.")
        return name
    @field_validator("description")
    @classmethod
    def ensure_description_non_empty(cls,descr:Any):
        if len(descr)==0:
            raise ValueError("Product description must be non-empty.")
        return descr
    @field_validator("price")
    @classmethod
    def ensure_price_is_positive(cls,price:Any):
        if price<=0:
            raise ValueError("Price must be positive.")
        return price
    @field_validator("stock")
    @classmethod
    def ensure_stock_is_positive(cls,stock:Any):
        if stock<=0:
            raise ValueError("Stock must be positive.")
        return stock    
@router.post("/")
async def add_product(product:ProductBody,db:AsyncSession=Depends(get_db)):
    result=await insert_product(db,product)
    if result==ResourceState.NewProduct:
        return JSONResponse(status_code=200,content={
            "result":"success",
            "message":f"Successfully added new product {product.name}"
        })
    else:
        return PlainTextResponse(status_code=500,content="Internal Server Error")
        
async def insert_product(db:AsyncSession,product:ProductBody)->ResourceState:
    new_product=Products(name=product.name,description=product.description,
                        price=product.price,stocks=product.stock)
    try:
        db.add(new_product)
        await db.commit()
        return ResourceState.NewProduct
    except Exception as e:
        print(f"Error : {e}")
        await db.rollback()
        return ResourceState.DataBaseFailure
    