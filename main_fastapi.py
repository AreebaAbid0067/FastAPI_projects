from fastapi import FastAPI

app = FastAPI()

@app.get("/adf") # frontend chahta hai backend say data lay ley
def get_hello_world():
    return {"Hello":"World"}

"""result=get_hello_world()
print(result)"""


@app.get("/login")
def get_hello_world():
    return{"Hello" : "World"}

@app.post("/login")
def get_hello_world():
    return{"Hello" : "World_login_post"}

@app.get("/auth/signup")
def get_hello_world1():
    return {"Hello" : "World"}

