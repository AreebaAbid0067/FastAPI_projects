from fastapi import FastAPI
from dotenv import load_dotenv
import os
from pymongo import MongoClient


app = FastAPI()
#optional: print(os.getenv("DB_URI"))
client = MongoClient(os.getenv("DB_URL"))

def get_db_client():
    try:
        client = MongoClient(os.getenv("DB_URL"))
        print("Connected to the database")
        return client
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

client = get_db_client()
db = client["fastapidb"] # type: ignore

@app.get("/")
def read_root():
    return {"status": "Server is running"}



@app.get("/todos")
def read_todos():
    try:
        todos = db.todos.find()
        listTodos = []
        for todo in todos:
            listTodos.append({
                "id": str(todo["_id"]),
                "title": todo["title"],
                "description": todo["description"],
                "status": todo["status"],
                "created_at": todo["created_at"],
            })
        return {
            "data": listTodos,
            "error": None,
            "message": "Todos read successfully",
            "status": "success"
            }
    except Exception as e:
        print(f"Error reading todos: {e}")
        return {
            "data": [],
            "error": "Error reading todos",
            "message": str(e),
            "status": "failed"
            }
        