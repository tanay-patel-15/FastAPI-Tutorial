from fastapi import FastAPI, Path
from typing import Optional

app = FastAPI()

inventory = {
  1: {
    "name": "Milk",
    "price": 3.99,
    "brand": "Regular"
  }
}

@app.get("/get-item/{item_id}")
def get_item(item_id: int= Path(description="The ID of the item you'd like to retrieve", gt=0, lt=2)):
  return inventory[item_id]


@app.get("/get-by-name/{item_id}")
def get_item(*, item_id:int, name: Optional[str] = None, test: int):
  for item_id in inventory:
    if inventory[item_id]["name"] ==  name:
      return inventory[item_id]
    else:
      return {"Data": "Not found"}