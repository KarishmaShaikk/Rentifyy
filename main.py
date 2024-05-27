from fastapi import FastAPI, Request , HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pyrebase import * 
import json
app = FastAPI()

origins = [
    "http://localhost:3000",
    # Add other origins if necessary
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
config = {
  "apiKey": "AIzaSyBtX9J_Unyn9JLud4u8snBBj2GbEDGfgcU",
  "authDomain": "renitfy.firebaseapp.com",
  "databaseURL": "https://renitfy-default-rtdb.firebaseio.com",
  "projectId": "renitfy",
  "storageBucket": "renitfy.appspot.com",
  "messagingSenderId": "1089896991584",
  "appId": "1:1089896991584:web:3b8b45d746a13da9baec05",
  "measurementId": "G-2XYJ9RXCE6"
}

firebase = initialize_app(config)
db = firebase.database()

auth = firebase.auth()

class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float = None

class Seller(BaseModel):
    firstname: str
    lastname: str
    email : str 
    phn : int
    password : str 
class Buyer(BaseModel):
    firstname: str
    lastname: str
    email : str 
    phn : int 
    password : str
class House(BaseModel):
    name : str
    place : str 
    area : str 
    price : int
    typeland : str
    typeliving : str
    description : str
class Login(BaseModel):
    email : str 
    password : str
@app.post("/login")
def sellerlogin(login: Login):
    try:
        user = auth.sign_in_with_email_and_password(login.email,login.password)
        data = db.child("sellers").child(user['localId']).get().val()
        if not (data) :
            data = db.child("buyer").child(user['localId']).get().val()
        return {"message": "login successful", "result": user['localId'] ,"data":data}
    except Exception as e:
        return {"message":"login unsuccessful" , "result":"kk"}
@app.post("/sellersingup/")
async def sellersingup(seller:Seller):
    try:
        data = seller.dict()
        data['password'] = ""
        user = auth.create_user_with_email_and_password(seller.email,seller.password)
        result = db.child("sellers").child(user["localId"]).set(data)
        return {"message": "Data added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/buyersingup/")
async def buyersingup(buyer:Buyer):
    try:
        data = buyer.dict()
        data['password'] = ""
        user = auth.create_user_with_email_and_password(buyer.email,buyer.password)
        result = db.child("buyer").child(user["localId"]).set(data)
        return {"message": "Data added successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/addhouse/{buyer_id}")
async def addhouse(buyer_id: str, house: House):
    try:
        buy_id = buyer_id
        result = db.child("house").child(buy_id).push(house.dict())
        return {"message": "Data added successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.delete("/deletehouse/{buyer_id}/{house_id}")
async def deletehouse(buyer_id: str,house_id : str):
    try:
        db.child("house").child(buyer_id).child(house_id).remove()
        return {"message": "Data deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get('/house/{seller_id}')
async def housse(seller_id:str):
    try:
        data = db.child("house").child(seller_id).get().val()
        return {"message": "Data added successfully", "result": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/allhouse")
async def allhouse():
    try :
        houses = db.child("house").get().val()
        fullhousese = dict()
        for i in houses:
            for j in houses[i]:
                fullhousese[j] = houses[i][j]
        return {"message": "all houses", "result": fullhousese}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/items/")
async def create_item(item: Item):
    return item

@app.post("/receive-json/")
async def receive_json(data: dict):
    return {"received_data": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
