import pytest
from routes import ResourceState
from routes.product import ProductBody,insert_product,get_all_products
from routes.oders import _place_oder
from .conftest import _test_db_session
from models.model import Products
@pytest.mark.asyncio
async def test_insert_product():
    product=ProductBody(name="Product3",description="Product3 Description",price=200.0,stock=10)
    async for db in _test_db_session():
        result=await insert_product(db,product)
    assert result==ResourceState.NewProduct
@pytest.mark.asyncio
async def test_get_all_products():
    product1 = Products(name="Product1",description="Product1 Description" ,price=10.0, stocks=100)
    product2 = Products(name="Product2",description="Product2 Description", price=20.0, stocks=200)
    async for db in _test_db_session():
        db.add_all([product1, product2])
        await db.commit()
        products = list(await get_all_products(db))

    assert len(products) == 2
    assert products[0].name == "Product1"
    assert products[1].price == 20.0
    assert products[0].description=="Product1 Description"
    assert products[1].stocks==200
@pytest.mark.asyncio
async def test_place_oder():
    product1 = Products(name="Laptop",description="Good Laptop" ,price=100.0, stocks=5)
    product2 = Products(name="Mobile",description="Good Mobile", price=50.0, stocks=10)
    async for db in _test_db_session():
        db.add_all([product1,product2])
        await db.commit()
        state1,result1=await _place_oder(db,{1:3,2:8}) # 3 Laptops & 8 Mobiles
        state2,result2=await _place_oder(db,{1:3,2:2}) # 3 Laptops & 2 Mobiles
        state3,result3=await _place_oder(db,{1:3,2:2}) # 3 Laptops & 2 Mobiles
        state4,result4=await _place_oder(db,{3:1}) # Non existent product
    assert state1==ResourceState.SufficientStock
    assert state2==ResourceState.PartiallySufficientStock
    assert state3==ResourceState.InsufficientStock
    assert state4==ResourceState.NonExistantProducts
    assert result1[0]["result"]=="success"
    assert result1[1]["result"]=="success"
    assert result2[0]["result"]=="failed"
    assert result2[1]["result"]=="success"
    assert result3[1]["result"]=="failed"
    assert result4[0]["result"]=="failed"

        
    