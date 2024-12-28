import requests
HOST="127.0.0.1"
PORT=8000
def test_app():
    base_url=f"http://{HOST}:{PORT}"
    test_product={
        "name":"Phone",
        "description":"Best Phone",
        "price":100.0,
        "stock":10
    }
    response1=requests.post(base_url+"/products",json=test_product)
    assert response1.status_code==200

    response2=requests.get(base_url+"/products")
    assert response2.status_code==200
    pid=response2.json()["products"][0]["id"]
    test_oder={
        "products":[{"product_id":pid,"quantity":1}]
    }
    response3=requests.post(base_url+"/oders",json=test_oder)
    assert response3.status_code==200
    test_oder={
        "products":[{"product_id":pid,"quantity":10}]
    }
    response4=requests.post(base_url+"/oders",json=test_oder)
    assert response4.status_code==409