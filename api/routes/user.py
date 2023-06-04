
from fastapi import APIRouter
from api.helpers.oauth import get_current_user
from bson import ObjectId

from api.models.user import User ,UserLogin ,User_update
from api.helpers.passHasser import Hash
from api.helpers.jwttoken import create_access_token
from api.schemas.user import userSchema
from fastapi import HTTPException, Depends, status
from ..db.dbConfig import collection
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/")
async def create_user(user:User):
  existUser=collection.find_one({"email":user.email})
  if existUser is not None:
    return {"message":"User already exists"}
  else:
    passwordHassed=Hash.bcrypted(user.password)
    user_object=dict(user)
    user_object["password"]=passwordHassed
    newUser= collection.insert_one(user_object)
    return  {
      "message": "Created new user",
    }


@router.post("/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
  email = form_data.username
  password = form_data.password

  users = collection.find_one({"email": email})
  print(users)
  if not users:
    return {"message": "Identifiant incorrect"}
  elif not Hash.verify(users["password"], form_data.password):
    return {"message": "Identifiant incorrect"}
  else:
    finder = userSchema(users)
    access_token = create_access_token(data={"sub": finder["id"]})
    return {"access_token": access_token, "token_type": "bearer"}




@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
  return current_user

@router.get("/")
async def get_all_users(current_user:User = Depends(get_current_user)):
   users = []
   for student in collection.find():
    users.append(userSchema(student))
   return users

@router.get("/{id}")
async def get_user_infos(id:str,current_user:User = Depends(get_current_user)):
   user=collection.find_one({"_id":id})
   if user is not None:
     return userSchema(user)


@router.put("/{id}")
async def update_user(id:str, user:User_update,current_user:User = Depends(get_current_user)):
  if ObjectId.is_valid(id):
    HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid user id provided")
  user_updated =collection.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(user) })
  if user_updated :
    return {
      "message": "User updated successfully "
    }

@router.delete("/{id}")
async def delete_user(id:str):
  if ObjectId.is_valid(id):
    HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid user id provided")
    collection.find_one_and_delete({"_id":ObjectId(id)})
    return {
      "message": "User deleted successfully "
    }
    