from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
  name: str
  price: float
  brand: Optional[str] = None

class UpdateItem(BaseModel):
  name: Optional[str] = None
  price: Optional[float] = None
  brand: Optional[str] = None

inventory = {}

@app.get("/get-item/{item_id}")
def get_item(item_id: int= Path(description="The ID of the item you'd like to retrieve", gt=0)):
  return inventory[item_id]


@app.get("/get-by-name")
def get_item(name: str = Query(None, title="Name", description="Name of the item.")):
  for item_id in inventory:
    if inventory[item_id].name ==  name:
      return inventory[item_id]

  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item name not found")
    


@app.post("/create-item/{item_id}")
def create_item(*, item_id: int = Path(description="The ID of the item you would like to view"), item: Item):
  if item_id in inventory:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item already exists")

  else:
    inventory[item_id] = item
    return inventory[item_id]
  


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
  if item_id not in inventory:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item name not found")

  
  if item.name != None:
    inventory[item_id].name = item.name

  if item.price != None:
    inventory[item_id].price = item.price

  if item.brand != None:
    inventory[item_id].brand = item.brand
  
  return inventory[item_id]


@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description= "ID of the item to be deleted")):
  if item_id not in inventory:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item name not found")

  else:
    del inventory[item_id]
    return {"Success":"Item has been successfully deleted!"}