# TASK 2:
# Implement an API endpoint to update (PATCH) a specific value in the DATA variable.
# Implement an API endpoint to delete (REMOVE) a specific field from the DATA variable.


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import uvicorn
import os
from typing import Optional

# Load environment variables
load_dotenv()

app = FastAPI(title="Simple FastAPI App", version="1.0.0")

data=[
    {"name": "Sam Larry", "age":20, "track": "AI Developer"},
    {"name": "Bahuballi", "age":21, "track": "Backend Developer"},
    {"name": "John Doe", "age":22, "track": "Frontend Developer"}
]



# Model for creating/replacing an item POST & PUT
class Item(BaseModel):
    name: str = Field(...,example="Perpetual")
    age: int = Field(...,example = 25)
    track: str = Field(...,example="Fullstack Developer")

# Model for partially updating an item (PATCH)
class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Perpetual")
    age: Optional[int] = Field(None, example=25)
    track: Optional[str] = Field(None, example="Fullstack Developer")



@app.get("/", description="This endpoint retuns a welcome messsage")
def root():
    return{"Message":"Welcome to my FastAPI Application"}

@app.get("/get_data", description = "Retrieving all data entries")
def get_data():
    return data

@app.post("/create_data", description="Creating a new data entry")
def create_data(req: Item):
    
    data.append(req.model_dump())
    print(data)
    return{"Message": "Data Received and Created", "Data": data}

@app.put("/update_data/{id}")
def update_data(id: int, req: Item):
    data[id] = req.dict()
    print(data)
    return {"Message":"Data Updated", "Data": data}

# PATCH and DELETE

@app.patch("/patch_data/{id}", description="Partially updating an existing data entry by (ID)")
def patch_data(id: int, req: ItemUpdate):
    if 0 <= id < len(data):
        current_item = data[id]
        update_data = req.model_dump(exclude_unset=True)

        # Update the existing dictionary with the new values
        current_item.update(update_data)

        print(data)
        return {"Message": f"Data at index {id} Partially Updated", "Data": current_item}
    else:
        raise HTTPException(status_code=404, detail=f"Item with index {id} not found.")

@app.delete("/delete_data/{id}", description="Delete a data entry by (ID)")
def delete_data(id: int):
    if 0 <= id < len(data):
        deleted_item = data.pop(id)
        print(data)
        return {"Message": f"Data at index {id} Deleted", "Deleted_Item": deleted_item}
    else:
        raise HTTPException(status_code=404, detail=f"Item with ID {id} not found.")



if __name__ == "__main__":
    print(os.getenv("host"))
    print(os.getenv("port"))
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))
