from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


user_db={
    'omar': {'username': 'omar', 'date_joined':'2021-12-01','location':'New york','age':28},
    'ahmed': {'username': 'ahmed', 'date_joined':'2021-12-02','location':'Palestine','age':19},
    'ali': {'username': 'ali', 'date_joined':'2021-12-03','location':'Toronto','age':52}
}


class User(BaseModel):
      username: str = Field(min_length=3, max_length=8)
      date_joined: date
      location:Optional[str]=None
      age:int = Field(None, gt=10, lt=100)

def check_username_exisit(username:str):
      if username not in user_db:
             raise HTTPException(status_code=404, detail=f'username {username} not found')

app = FastAPI()

@app.get('/')
def get_users():
    user_list = list(user_db.values())
    return user_list


@app.get('/users')
def get_users_query(limit:int=20):
    user_list = list(user_db.values())
    return user_list[:limit]


@app.get('/users/{username}')
def get_users_path(username :str):
      # if username not in user_db:
      #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
      check_username_exisit(username)
      return user_db[username]
   

@app.post('/users')
def create_user(user:User):
      username=user.username
      if username in user_db:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT , detail=f'cannot create user {username} already exist')
      user_db[username]= user.dict()
      return {'message:' f'successfuly created user {username}'}


@app.delete('/users/username')
def delete_user(username:str):
      check_username_exisit(username)
      del user_db[username]
      return {'message' f'successfully deleted user {username}'}

@app.put('/users')
def update_user(user:User):
      username=user.username
      user_db[username]= user.dict()
      return {'message:' f'successfuly updated user {username}'}

@app.patch('/users')
def update_user_partcialy(user:User):
      username=user.username
      user_db[username].update(user.dict(exclude_unset= True))
      return {'message:' f'successfuly updated partcially user {username}'}