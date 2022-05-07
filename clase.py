#Python 
from typing import Optional
from enum import Enum
#Pydantic
from pydantic import BaseModel
from pydantic import Field, EmailStr, PaymentCardNumber
# FastAPI
from fastapi import FastAPI
# Body permite aclarar que un parametro de entrada es de tipo Body 
from fastapi import Body, Query, Path, status, Form 

app = FastAPI()

class LoginOut(BaseModel):
    username: str = Field(
        ...,
        max_length=20,
        example="francodem"
    )
    message: str = Field(default="Login succesfully!")
    

class Error1(BaseModel):
    message: str = Field(default="Error on message")

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
        max_length=50,
        example="Franco"
    )
    last_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example="Moreno"
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=26
    )
    hair_color: Optional[HairColor] = Field(
        default=None,
        example=HairColor.red
    )
    is_married: Optional[bool] = Field(default=None, example=True) 
    email: EmailStr = Field(
        ...,
        example="francomorenoq@gmail.com"
    )
    credit_card_number: PaymentCardNumber = Field(
        ...,
        min_length=16,
        max_length=16,
        example="1234567891234567"
    )
    
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Franco",
    #             "last_name": "Moreno",
    #             "age": 26,
    #             "hair_color": "brown",
    #             "is_married": True,
    #             "email": "francomorenoq@gmail.com",
    #             "credit_card_number": "1234567891234567"
    #         }
    #     }


class PassPerson(Person):
    password: str = Field(
        ...,
        min_length=8,
        example="12345678"
    )
    
    
class PersonOut(Person):
    pass


class LocationExample(Enum):
    city = "Ensenada" 
    state = "Baja"
    country = "Mexico"


class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example=LocationExample.city
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example=LocationExample.state
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example=LocationExample.country
    )
    

@app.get(
    "/",
    status_code=status.HTTP_200_OK
    )
def home():
    return {"Hello":"World"}


# Request and Response Body 
@app.post(
    "/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: PassPerson = Body(...)):
    # (...) Parametro o atributo obligatorio 
    return person 


# Validaciones: Query Parameters 
@app.get("/person/detail", status_code=status.HTTP_200_OK)
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="""This is the person name. 
        It's between 1 and 50 characters""",
        example="Rocio"
        ),
    age: int = Query(
        ...,
        gt=0,
        title="Person age",
        description="""This is the person age. 
        It's required""",
        example=35
        )
):
    return {f'hello, {name}': age}


# Validaciones: Path Paramaters
@app.get("/person/detail/{person_id}", status_code=status.HTTP_200_OK)
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title="Person id",
        description="This is the person id")
):
    return {person_id: "It exists!"}


@app.put("/person/{person_id}", status_code=status.HTTP_202_ACCEPTED)
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
    return person 


@app.post(
    path="/login",
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form(...)):
    # Modelo de Pydantic es un objeto, se debe instanciar con los atributos 
    # Se envia username unicamente, y se retorna los objetos del modelo 
    response = LoginOut(
        username=username
        )
    
    if response.username == "franco":
        return response
    elif response.username == "laura":
        response = Error1()
        return response
    else:
        return {'response':'Error'}
