from sqlalchemy import Column,BigInteger,String,Float,Text,Integer,Enum,ForeignKey
from sqlalchemy.orm import relationship
import enum
from typing import Dict,Union
from . import Base

class Products(Base):
    __tablename__='products'
    id=Column(BigInteger,primary_key=True,autoincrement=True)
    name=Column(String(100),nullable=False)
    description=Column(Text)
    price=Column(Float,nullable=False)
    stocks=Column(Integer,nullable=False,default=1)
    oders=relationship('Oders',secondary='oder_product',back_populates='products',viewonly=True)
    oder_product=relationship('OderProduct',back_populates='product')
    
    def __repr__(self):
        return f"Product< Id : {self.id}, Name : {self.name}, Price : {self.price}, Stock : {self.stocks} >"
    
    def to_dictionary(self)->Dict[str,Union[int,float,str]]:
        data={}
        data["id"]=self.id
        data["name"]=self.name
        data["description"]=self.description
        data["price"]=self.price
        data["stocks"]=self.stocks
        return data    
    

class OderStatus(str,enum.Enum):
    COMPLETED="completed"
    PENDING="pending"

class Oders(Base):
    __tablename__='oders'
    id=Column(BigInteger,primary_key=True,autoincrement=True)
    total_price=Column(Float,nullable=False)
    status=Column(Enum(OderStatus),default=OderStatus.PENDING,nullable=False)
    products=relationship('Products',secondary='oder_product',back_populates='oders',viewonly=True)
    oder_product=relationship('OderProduct',back_populates='oder',cascade='delete')

    def __repr__(self):
        return f"Oder< Id : {self.id}, Total Price : {self.total_price}, Status : {self.status}>"
    
    def to_dictionary(self)->Dict[str,Union[int,float,str]]:
        data={}
        data["id"]=self.id
        data["total_price"]=self.total_price
        data["status"]=str(self.status)
        return data

class OderProduct(Base):
    __tablename__='oder_product'
    oder_id=Column(BigInteger,ForeignKey('oders.id'),primary_key=True)
    product_id=Column(BigInteger,ForeignKey('products.id'),primary_key=True)
    quantity=Column(Integer,nullable=False,default=1)
    oder=relationship('Oders',back_populates='oder_product')
    product=relationship('Products',back_populates='oder_product')
    
    def __repr__(self):
        return f"OderProduct< Oder Id : {self.oder_id}, Product Id : {self.product_id}, Quantity : {self.quantity}>"


