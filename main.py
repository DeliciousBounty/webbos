from typing import ItemsView, Union
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from urllib import request


class Person(BaseModel):
    name: str = Field(..., description="Name of the Person",
                      max_length=100, example="John Doe")
    age: int = Field(..., description="Age of the Person",
                     minimum=0, maximum=120, example=30)


app = FastAPI()

@app.get("/")
async def root():
    return "Hello"


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]


@app.post("/int_min_max/")
async def int_min_max(person: Person):
    return f"Hello {person.name} you are {person.age} years old"


@app.put("/int_min_max/")
async def int_min_max():
    return f"Shadow API endpoint, I shouldn't be accessed"


@app.post("/str_max/")
async def str_max(person: Person):
    return f"Hello {person.name} your name is {len(person.name)} chars long"


@app.get("/redirect/")
async def redirect(location: str):
    if len(location) == 0:
        return {"error": "location is empty"}
    with request.urlopen(location) as ret:
        return ret.read()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
