from fastapi import FastAPI
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime 
from pydantic import BaseModel

from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
print(os.getenv("DB_URL"))

class Details(BaseModel):  # this defines what data my API expects
    name:str
    age:str
    occupation:str


def get_db_client():
    try:
        client = MongoClient(os.getenv("DB_URL"))
        print("connected to database successfully")
        return client
    
    except Exception as e:
        print(f"Error connecting to the db")
        return None
    
client = get_db_client()
db = client["fastapidb"]

@app.get("/")
def read_root():
    return {
        "status":"Server is running"
    }

@app.get("/get_details") # read operation code
def read_details():
    try:
        details = db.student_details.find()
        Details = []

        for std in details:
            Details.append({
                "id":str(std["_id"]),
                "name": str(std["name"]),
                "age"  : str(std["age"]),
                "occupation": str(std["occupation"])                                 
            })

        return {
            "data":Details,
            "error":None,
            "message":"Details read successfully",
            "status":"success"
        }
    
    except Exception as e:
        print(f"Error reading details: {e}")
        return {
            "data" : [],
            "error":"Error reading details",
            "message" : str(e),
            "status" : "failed"
        }
    
@app.get("/get_details_specific/{id}") # read specific
def read_details_by_id(id:str):
    print(id)
    try:
        details = db.student_details.find_one({"_id":ObjectId(id)})
        if details is None:
            return{
                "data": {},
                "error" : "details not found",
                "message" :"details not found",
                "status":"failed"
            }
        
        return{
            "data" : {
                "id" : str(details["_id"]),
                "name": str(details["name"]),
                "age" : str(details["age"])
            },
            "error" : None,
            "message" : "details read successfully",
            "status" : "success"
        }
    
    except Exception as e:
        print("error reading details {e}")
        return{
            "data" : {},
            "error" : "Error reading details",
            "message" : "error!",
            "status" : "failed"
        }
    
    
@app.post("/create_std")
def create_details(name: str, age: str, occupation: str):
    try:
        result = db.student_details.insert_one({
            "name": name,
            "age": age,
            "occupation" :occupation
        })

        return{
            "data" : {"id":str(result.inserted_id)},
            "error" : None,
            "message" : "Record created successfully",
            "status" : "success"
        
        }
    
    except Exception as e:
        print(f"error creating std: {e}")
        return{
            "data ": {},
            "error" : "error creating record",
            "message":str(e),
            "status":"failed"
        }
    

"""
GET is used when u want to fetch or read data...
POST is used when u wnat to send or create data
"""


@app.delete("/delete_record/{id}")
def delete_record(id:str):
    try:
        result = db.student_details.delete_one({"_id":ObjectId(id)})
        if result.deleted_count == 0:  # if no record with that id found
            return{
                "data":{},
                "error":"record not found",
                "message":"sorry record not found",
                "status":"failed"
            }
        
        return{
            "data":{},
            "error" : None,
            "message" : "record deleted successfully"
        }
    
    except Exception as e:
        print(f"Error deleting record: {e}")
        return{
            "data":{},
            "error":str(e),
            "message":"error deleting the record",
            "status":"failed"
        }
    
@app.put("/update_record/{id}")
def update_record(id:str,detail:Details):
    try:
        result = db.student_details.update_one(
            {"_id":ObjectId(id)},
            {
                "$set":{
                    "name":detail.name,
                    "age":detail.age,
                    "occupation":detail.occupation
                }
            }
        )
        if result.modified_count == 0:
            return{
                "data":{},
                "message":"record with this ID doesnt exist"
            }
        
        return{
            "data":{},
            "error":None,
            "message":"record updated successfully"
        }
        
    except Exception as e:
        print(f"record counldnt be edited")
        return{
            "data":{},
            "message":str(e),
            "status":"failed"
        }
        
        
