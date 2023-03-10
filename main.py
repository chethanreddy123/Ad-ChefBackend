import re
import math
from collections import Counter
from urllib import request
import pandas as pd
from fastapi import FastAPI, Request, Query
from typing import Optional
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json
from fastapi.encoders import jsonable_encoder
import joblib
import datetime
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
    print(DataIn)

    if len(DataIn) > 0:
        return {"Status" : "User already exsists"}



    Data = {
        "CreatedAt" : infoDict["CreatedAt"],
        "User_Id" : infoDict["ID"],
        "Email_Id" : infoDict["Email_Id"],
        "Name" : infoDict["Name"],
        "TypeOfSub" : "Free",
        "Token_Left_CurrMonth" : 5, # Left tokens for the month
        "Total_Token_CurrMonth" : 5,  # total token for current month
        "Tokens_per_month" : 5, # based on the subscription
        "Total_Token_Spent" : 0, # all the tokens spent till date
        "Fov_Ads" : [],
        "Ads_List" : [],
        "imgURL" : infoDict['imgURL']

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
    print(infoDict)



    DataIn = list(UserData.find({"Email_Id" : infoDict["Email_Id"]}))
    print(DataIn)

    if len(DataIn) == 0:
        return {"Status" : "User doesn't exists"}

    DataIn = list(UserData.find({"Email_Id" : infoDict["Email_Id"]}))
    
    myInfo = DataIn[0]

    del myInfo["_id"]

    return myInfo


@app.post("/ad_creation/")
async def ad_creation(info : Request):
    print(await info.body())
    infoDict = await info.json()
    infoDict = dict(infoDict)

    myquery = { "User_Id": infoDict["User_Id"] }
    newvalues = { "$set": { "Token_Left_CurrMonth":  infoDict["Token_Left_CurrMonth"] } }

    x = UserData.update_one(myquery, newvalues)

    adList = UserData.find_one({"User_Id": infoDict["User_Id"]})["Ads_List"]
    adList.append({
        "Creation_Time" :  datetime.datetime.now(),
        "Name_of_Company" : infoDict["Name_of_Company"],
        "Type_of_Company" : infoDict["Type_of_Company"],
        "USP" : infoDict["USP"],
        "Tone" : infoDict["Tone"],
        "Details" : infoDict["Details"],
        "Platform" : infoDict["Platform"],
        "Prompt" : infoDict["Prompt"],
        "Ad_Copy" : infoDict["Ad_Copy"],
    })

    print(adList)


    myquery = { "User_Id": infoDict["User_Id"] }
    newvalues = { "$set": { "Ads_List":  adList} }

    x = UserData.update_one(myquery, newvalues)


    myquery = { "User_Id": infoDict["User_Id"] }
    newvalues = { "$set": { "Total_Token_Spent" :  infoDict["Total_Token_Spent"]} }

    x = UserData.update_one(myquery, newvalues)


    if x.modified_count:
        return {"Status" : "successful"}
    else:
        return {"Status" : "unsuccessful"}


@app.post("/fov_ad/")
async def fov_ad(info : Request):
    print(await info.body())
    infoDict = await info.json()
    infoDict = dict(infoDict)

    myquery = { "User_Id": infoDict["User_Id"] }

    adList = UserData.find_one({"User_Id": infoDict["User_Id"]})["Fov_Ads"]
    adList.append(infoDict["Ad_string"])

    newvalues = { "$set": { "Fov_Ads" :  adList } }

    x = UserData.update_one(myquery, newvalues)


    if x.modified_count:
        return {"Status" : "successful"}
    else:
        return {"Status" : "unsuccessful"}