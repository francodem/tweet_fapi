#Python 
from typing import Optional
from enum import Enum
#Pydantic
from pydantic import BaseModel
from pydantic import Field, EmailStr, PaymentCardNumber
# FastAPI
from fastapi import FastAPI
# Body permite aclarar que un parametro de entrada es de tipo Body 
from fastapi import Body, Query, Path

app = FastAPI()

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


# Models 
class Person(BaseModel):
    first_name: str = Field(
        ..., 
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ..., 
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    hair_color: Optional[HairColor] = Field(
        default=None
    )
    is_married: Optional[bool] = None 
    email: EmailStr = Field(
        ...
    )
    credit_card_number: PaymentCardNumber = Field(
        ...,
        min_length=16,
        max_length=16
    )


class Location(BaseModel):
    city: str = Field(
        ..., 
        min_length=1,
        max_length=50
    )
    state: str = Field(
        ..., 
        min_length=1,
        max_length=50
    )
    country: str = Field(
        ..., 
        min_length=1,
        max_length=50
    )
    

@app.get("/")
def home():
    return {"Hello":"World"}


# Request and Response Body 
@app.post("/person/new")
def create_person(person: Person = Body(...)):
    # (...) Parametro o atributo obligatorio 
    return Person 


# Validaciones: Query Parameters 
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="""This is the person name. 
        It's between 1 and 50 characters"""
        ),
    age: int = Query(
        ...,
        gt=0,
        title="Person age",
        description="""This is the person age. 
        It's required"""
        )
):
    return {f'hello, {name}': age}


# Validaciones: Path Paramaters
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title="Person id",
        description="This is the person id")
):
    return {person_id: "It exists!"}


@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    response = person.dict()
    response.update(location.dict())
    return response 