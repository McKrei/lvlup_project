from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse

from fastapi import status

from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    username: str
    email: str | None = None
    password: str


app = FastAPI()


users = [
    {"user_id": 1, "username": "user1", "email": "asd@sadk.ru", "password": "123"},
    {"user_id": 2, "username": "user3", "email": "asd@sadk.ru", "password": "214"},
    {"user_id": 3, "username": "user4", "email": "asd@sadk.ru", "password": "224"},
    {"user_id": 4, "username": "adsfas", "email": "asd@sadk.ru", "password": "55"},
]


async def get_user(user_id: int):
    for user in users:
        if user["user_id"] == user_id:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.get("/users/", response_model=list[User])
async def read_users():
    return users


@app.get("/users/{user_id}", response_model=User)
async def read_user(user: User = Depends(get_user)):
    return user


@app.post("/users/", response_model=User)
async def create_user(user: User):
    users.append(user.dict())
    return user.dict()


@app.put("/users/{user_id}", response_model=User)
async def update_user(
    user: User = Depends(get_user), username: str = None, email: str = None, password: str = None
):
    user["username"] = username or user["username"]
    user["email"] = email or user["email"]
    user["password"] = password or user["password"]
    return user


@app.delete("/users/{user_id}")
async def delete_user(user: User = Depends(get_user)):
    users.remove(user.dict())
    return status.HTTP_204_NO_CONTENT

