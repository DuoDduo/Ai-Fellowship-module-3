from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
import uvicorn


app=FastAPI(title="Simple FastAPI App", version="1.0.0")

@app.get("/", description="This enpoint retuns a welcome messsage")
def root():
    return {"message":"Hello World"}

@app.get("/posts")
def get_posts():
    return{"data":"This is my study posts"}
@app.post("/createpost")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new_post":f"title: {payload['title']} content:{payload['content']}"}

if __name__  == "__main__":
    uvicorn.run(app)