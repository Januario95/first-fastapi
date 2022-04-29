from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import (
    get_redis_connection, HashModel
)
from starlette.requests import Request
from typing import Optional
import requests


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)


redis = get_redis_connection(
    host='redis-12258.c16.us-east-1-3.ec2.cloud.redislabs.com',
    port=12258,
    password='AYHMUoMJDoeDJpsWYLxUysq3mtsUVwlB',
    decode_responses=True
)


class Product(HashModel):
    name: str
    price: float
    quantity: int
    descount: Optional[float] = None

    class Meta:
        database = redis



def format_obj(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity,
        'descount': product.descount
    }


@app.get('/products')
async def all():
    return [format_obj(pk) for pk in Product.all_pks()]


@app.post('/products')
async def create(request: Request):
    data = await request.json()
    name = data['name']
    price = data['price']
    quantity = data['quantity']
    descount = data['descount']

    product = Product(
        name=name,
        price=price,
        quantity=quantity,
        descount=descount
    )
    product.save()

    return product

@app.get('/products/{pk}')
async def get(pk: str):
    return Product.get(pk)


@app.delete('/products/{pk}')
async def delete(pk: str):
    return Product.delete(pk)

# @app.patch('/products/{pk}')
# async def patch(request: Request):
#     body = await request.json()
#     print(body)

    # product = Product.get(pk)
    # return {}

