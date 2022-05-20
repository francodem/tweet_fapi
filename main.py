# Python
from typing import Optional
from typing import List
from uuid import UUID
import uuid
from datetime import datetime 
from datetime import date
import json 

# Pydantic 
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body 
from fastapi import Path


app = FastAPI()

# Models //////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(
        ...,
        example="user@gmail.com"
        )


class UserLogin(UserBase):
    password: str = Field(
    ...,
    min_length=8
    )

 
class User(UserBase):
    user_id: UUID = Field(...)
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
    birth_date: Optional[date] = Field(
        default=None
    )


class UserRegister(User):
    password: str = Field(
    ...,
    min_length=8
    )
    
    
class Tweet(BaseModel):
    tweet_id: UUID = Field()
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(deault=None)
    by: User = Field(...)


# Path ops //////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# To show all users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
    )
def show_all_users():
    """
    This path operation shows all users in the app 
    
    Parameters:
        - NA
    
    Return a json list with all users in the ap, with the following keys; 
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results 


# To show only a one user 
@app.get(
    path="/users/{user_name}",
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["Users"]
    )
def show_a_user(user_name: str = Path(
    ...,
    min_length=1,
    max_length=50,
    title="This is the first name of the user",
    description="Here you can enter a user's first name to find a specific user",
    example="laura"
)):
    '''
    Show a user by name 
    
    This path operation is to show a user by name 
    
    Parameters: 
        - user_name
        
    Returns a json with the basic user informaiton: 
        tweet_id: UUID
        content: str
        created_at: datetime 
        updated_at: Optional[datetime]
        by: User
    
    Returns in error case:
        - json response with the error 
    '''
    with open("users.json", encoding="utf-8") as f:
        results = json.loads(f.read())
        for i in range(0, len(results)):
            if results[i]["first_name"] == user_name:
                return results[i]
    return {"Error": f"User {user_name} is not exists"}


# To register a user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a user",
    tags=["Users"]
    )
def signup(user: UserRegister = Body(...)):
    '''
    Signup
    
    This path operation register a user in the app 
    
    Parameters:
        - Request body parameter
            - user: UserRegister
    
    Returns a JSON with the basic information:
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_day: str
    '''
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.load(f)
        print(results)
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        # This is for moving into the document 
        f.seek(0)
        json.dump(results, f)
        return user 


# To login a user
@app.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    tags=["Users"]
    )
def login(user_login: UserLogin = Body(...)):
    '''
    User Login Path Op
    
    Here the user can enter your information for login in the app
    
    Parameters:
        - user_id: UUID
        - email: EmailStr
        - password: str
    
    Return:
        - Returns a welcome message if the login is correct 
        - Returns a warning message if the login is incorrect 
    '''
    with open("users.json", "r+", encoding="utf-8") as f:
        data = json.loads(f.read())
        user_login = user_login.dict()
        for i in range(0,len(data)):
            if data[i]["email"] == user_login["email"]:
                if data[i]["password"] == user_login["password"]:
                    return {"Correct login": "Welcome"} 
                else: 
                    return {"Warning": "Invalid password"}  
        return {"Warning": "User not exists"}  
    
    
# To update a user 
@app.put(
    path="/signup/{user_name}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update a user",
    tags=["Users"]
    )
def update_a_user(
    user_name: str = Path(...),
    user_update: UserRegister = Body(...)
):
    '''
    Update User Path Operation 
    
    Here you can update a user with your new personal information 
    
    Parameters:
        - user_id: UUID
        - first_name: str
        - last_name: str
        - email: EmailStr
        - password: str 
        - birthday: date 
    
    Returns:
        - If the user exists, the app returns an OK message 
        - If user not exists, the app returns an error 
    '''
    with open("users.json", "r+", encoding="utf-8") as f:
        data = json.load(f)
        user_update = user_update.dict()
        user_update["user_id"] = str(user_update["user_id"])
        user_update["birth_date"] = str(user_update["birth_date"])
        for user in data:
            if user["first_name"] == user_name:
                data[data.index(user)] = user_update
                f.seek(0)
                f.truncate(0)
                print(data)
                json.dump(data, f)
                return {"OK": "Modification applied"}
              
        return {"Warning": "User not exists"}  
        

# To delete a user 
@app.delete(
    path="/signup/{first_name}/delete",
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"]
    )
def delete_a_user(first_name: str = Path(
    ...,
    min_length=1,
    max_length=50,
    example="franco"
    )):
    '''
    Delete user section 
    
    Delete user path operation
    
    Parameters:
        -   first_name: str  
        
    Return: 
        -   If user exists; returns a deletion message 
        -   If user not exists; return an error 
    
    '''
    with open("users.json", "r+", encoding="utf-8") as f:
        data = json.load(f)
        for i in range(len(data)):
            if first_name == data[i]["first_name"]:
                data.remove(data[i])
                f.seek(0)
                f.truncate(0)
                json.dump(data, f)
                return {"Success": f"User {first_name} deleted"}
        return {"Error": f"User {first_name} not exists"}


# Tweets //////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Show all tweets 
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
    )
def home():
    '''
    Show all tweets
    
    This path operation is to show all tweets 
    
    Parameters: 
        - na
        
    Returns a json with the basic tweet informaiton: 
        tweet_id: UUID
        content: str
        created_at: datetime 
        updated_at: Optional[datetime]
        by: User
    '''
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results
        

# Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweets",
    tags=["Tweets"]
    )
def post(tweet: Tweet = Body(...)):
    '''
    Post a Tweet 
    
    This path operation is to post a tweet in the app 
    
    Parameters: 
        - Request Body Parameter
            - tweet: Tweet 
        
    Returns a json with the basic tweet informaiton: 
        tweet_id: UUID
        content: str
        created_at: datetime 2
        updated_at: Optional[datetime]
        by: User
    '''
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])

        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet
    

# Show a tweet 
@app.get(
    path="/tweets/{tweet_id}",
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
    )
def show_a_tweet(tweet_id: UUID = Path(...)):
    '''
    View a tweet section 
    
    At this path operation it can be show a tweet
    
    Parameters: 
        -   tweet_id: UUUID

    Return:
        - If the tweet_id exists; return the tweet 
        - If tweet_id not exists; return an error 
    '''
    with open("tweets.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for i in range(len(data)):
            if str(tweet_id) == data[i]["tweet_id"]:
                return data[i]    
        return {"Error": "tweet_id not exists"}


# Delete a tweet 
@app.delete(
    path="/tweets/{tweet_id}/delete",
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
    )
def delete_a_tweet(tweet_id: UUID = Path(...)):
    '''
    Delete a tweet 
    
    At this path operation it can be deleted a tweet 
    
    Parameters: 
        -   tweet_id: UUUID

    Return:
        - If the tweet_id exists; return a delete message 
        - If tweet_id not exists; return an error 
    '''
    with open("tweets.json", "r+", encoding="utf-8") as f:
        data = json.load(f)
        for i in range(len(data)):
            if str(tweet_id) == data[i]["tweet_id"]:
                data.remove(data[i])
                f.seek(0)
                f.truncate(0) 
                json.dump(data, f) 
                return {"OK": f"Tweet from {tweet_id} has been deleted"} 
        return {"Error": "tweet_id not exists"}


# Update a tweet 
@app.put(
    path="/tweets/{tweet_id}/update",
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
    )
def update_a_tweet(tweet_id: UUID = Path(...), 
                   tweet: Tweet = Body(...)
    ):
    '''
    Update a tweet section 
    
    At this path operation it can be updated a tweet
    
    Parameters: 
        -   tweet_id: UUUID

    Return:
        - If the tweet_id exists; return the updated tweet 
        - If tweet_id not exists; return an error 
    '''
    with open("tweets.json", "r+", encoding="utf-8") as f:
        data = json.load(f)
        tweet = tweet.dict()
        tweet["tweet_id"] = str(tweet["tweet_id"])
        tweet["created_at"] = str(tweet["created_at"])
        tweet["updated_at"] = str(tweet["updated_at"])
        tweet["created_at"] = str(tweet["created_at"])
        tweet["by"]["user_id"] = str(tweet["by"]["user_id"])
        tweet["by"]["birth_date"] = str(tweet["by"]["birth_date"])
        for i in range(len(data)):
            if str(tweet_id) == data[i]["tweet_id"]:
                if str(tweet["tweet_id"]) == data[i]["tweet_id"]:
                    data.remove(data[i])
                    data.append(tweet)
                    f.seek(0)
                    f.truncate(0)
                    json.dump(data, f)
                    return {"OK": "Tweet has been updated"}    
                else:
                    return {"Error": "Tweet updated should have the same ID"}    
        return {"Error": "tweet_id not exists"}