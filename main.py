import re
import math
from collections import Counter
from urllib import request
import pandas as pd
from fastapi import FastAPI, Request, Query
from typing import Optional
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
import json
from fastapi.encoders import jsonable_encoder
import joblib
from pymongo.mongo_client import MongoClient

ConnectData = MongoClient("mongodb://aioverflow:1234@ac-pu6wews-shard-00-00.me4dkct.mongodb.net:27017,ac-pu6wews-shard-00-01.me4dkct.mongodb.net:27017,ac-pu6wews-shard-00-02.me4dkct.mongodb.net:27017/?ssl=true&replicaSet=atlas-jcoztp-shard-0&authSource=admin&retryWrites=true&w=majority")
UserData = ConnectData.Ad_Chef.userData



app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/new_user/")
async def new_user(info : Request):
    print(await info.body())
    infoDict = await info.json()
    infoDict = dict(infoDict)

    DataIn = list(UserData.find({"Email_Id" : infoDict["Email_Id"]}))

    if len(DataIn) == 1:
        return {"Status" : "User already exsists"}



    Data = {
        "User_Id" : 122423,
        "Email_Id" : infoDict["Email_Id"],
        "Name" : infoDict["Name"],
        "TypeOfSub" : None,
        "No_Tokens" : None,
        "Fov_Ads" : [],
        "Ads_List" : []
    }

    try:
        Check = UserData.insert_one(Data)
        return {"Status" : "Successful"}
    except Exception as e:
        return {"Status" : e}

    




@app.post("/login_check/")
async def new_user(info : Request):
    print(await info.body())
    infoDict = await info.json()
    infoDict = dict(infoDict)





    
