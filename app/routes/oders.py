from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse,PlainTextResponse
from pydantic import BaseModel,field_validator
from typing import List,Dict,Any,Union,Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.model import Oders,Products,OderProduct,OderStatus
from database.db import get_db
from . import ResourceState

router=APIRouter()

class ProductDetails(BaseModel):
    product_id:int
    quantity:int

    # Validators
    @field_validator('product_id')
    @classmethod
    def ensure_non_negetive_pid(cls,pid:Any):
        if pid<0:
            raise ValueError("Product Id must be non-negetive.")
        return pid
    @field_validator('quantity')
    @classmethod
    def ensure_positive_quantity(cls,quant:Any):
        if quant<=0:
            raise ValueError("Quantity must be greater than zero.")
        return quant

class OderBody(BaseModel):
    products:List[ProductDetails]
    
    # Validators
    @field_validator('products')
    @classmethod
    def ensure_non_empty_products(cls,prod:Any):
        if len(prod)==0:
            raise ValueError("products list must be non empty.")
        return prod

@router.post("/")
async def place_oders(order:OderBody,db:AsyncSession=Depends(get_db)):
    required_products:Dict[int,int]={}

    # Creating a dictionary from product list of current oder with schema {"required_product_id" : "quantity"}
    # This way if multiple products with same id exists then we can aggregate them.
    for product in order.products:
        if product.product_id not in required_products:
            required_products[product.product_id]=product.quantity
        else:
            required_products[product.product_id]+=product.quantity
    
    state,oder_result= await _place_oder(db,required_products)
    # Inventory has sufficient amount of all products
    if state==ResourceState.SufficientStock:
        return JSONResponse(status_code=200,content={
            "oder_result":oder_result
        })
    # No product in current oder exists
    elif state==ResourceState.NonExistantProducts:
        return JSONResponse(status_code=404,content={
            "oder_result":oder_result
        })
    # Some database error happened.
    elif state==ResourceState.DataBaseFailure:
        return PlainTextResponse(status_code=503,content="Internal Server Error")
    else:
        # We can only place oder for some of the products others are insufficient.
        return JSONResponse(status_code=409,content={
            "oder_result":oder_result
        })

async def _place_oder(db:AsyncSession,required_products:Dict[int,int])->Tuple[ResourceState,List[Dict[str,Union[str,int]]]]:
    result=[]
    oder=Oders(total_price=0,status=OderStatus.COMPLETED)
    resource_state=ResourceState.SufficientStock
    product_existance_flag=False # If no product in oder list exists it will stay false.
    db.add(oder)
    for product_id,quantity_required in required_products.items():
        cur_result={}
        product_query_result=await db.execute(select(Products).filter_by(id=product_id))
        product=product_query_result.scalar_one_or_none()
        if product==None:
            cur_result["product_id"]=product_id
            cur_result["result"]="failed"
            cur_result["message"]=f"Product doesn't exist."
        
        elif product.stocks>=quantity_required:
            product.stocks-=quantity_required
            oder.total_price+=(product.price*quantity_required)
            oder_product=OderProduct(oder=oder,product=product,quantity=quantity_required)
            db.add(oder_product)
            cur_result["product_id"]=product_id
            cur_result["result"]="success"
            cur_result["message"]=f"Oder placed for {quantity_required} {product.name}(s)."
            product_existance_flag=True
        else:
            oder.status=OderStatus.PENDING
            resource_state=ResourceState.PartiallySufficientStock
            cur_result["product_id"]=product_id
            cur_result["result"]="failed"
            cur_result["message"]=f"Insufficient Stock. Current available stock : {product.stocks}"
            product_existance_flag=True
        result.append(cur_result)
    
    if not product_existance_flag:
        return ResourceState.NonExistantProducts,result
    
    if oder.total_price==0:
        resource_state=ResourceState.InsufficientStock
    try:
        await db.commit()
    except:
        await db.rollback()
        resource_state=ResourceState.DataBaseFailure
    return resource_state,result

        
