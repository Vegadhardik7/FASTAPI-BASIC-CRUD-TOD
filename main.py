from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import uuid4

app = FastAPI()

data = [{"id":"123","uname":"qwe","todo":"write blog"},{"id":"345","uname":"mewmew","todo":"write books"}]

class UserModel(BaseModel):
    uname: str = Field(..., min_length=1, max_length=50)
    todo: str | None = Field(None, max_length=255)

class UpdateUserModel(BaseModel):
    uname: str | None = None
    todo: str | None = None

class User:
    def __init__(self, uname:str, todo:str|None=None):
        self.id = str(uuid4())
        self.uname = uname
        self.todo = todo

# get all data
@app.get("/", response_class=JSONResponse)
async def getData():
    return data

# get data by id
@app.get("/id/{value}", response_class=JSONResponse)
async def getDataByID(value: str):
    for item in data:
        if item['id'] == value:
            return item
    raise HTTPException(status_code=500, detail=f"User with ID '{value}' not found")
    
# create a user
@app.post("/createusr", response_class=JSONResponse)
async def createUser(user:UserModel):
    new_usr = User(uname=user.uname, todo=user.todo)

    data.append({"id":str(new_usr.id), "uname":new_usr.uname, "todo":str(new_usr.todo)}) 

    return {"message": "User created successfully", "data":data}

# udpate a user based on id
@app.put("/updatedata/{usr_id}", response_class=JSONResponse)
async def updateUser(usr_id: str, user: UpdateUserModel):
    for usr in data:
        if usr['id'] == usr_id:
            if user.uname is not None:
               usr["uname"] = user.uname
            if user.todo is not None:
               usr["todo"] = user.todo
            return {"message": "User updated successfully", "data": usr}

    # If user is not found, raise a 404 error
    raise HTTPException(status_code=404, detail=f"User with ID '{usr_id}' not found") 

# delete a user based on id
@app.delete("/delete/{user_id}",response_class=JSONResponse)
async def deleteUser(usr_id: str):
    for usr in data:
        if str(usr["id"]) == usr_id:
            data.remove(usr)
            return {"message": "User deleted successfully"}
    
    # If no user is found with the given ID, raise a 404 error
    raise HTTPException(status_code=404, detail=f"User with ID '{usr_id}' not found")