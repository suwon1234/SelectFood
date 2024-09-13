from fastapi import FastAPI, Header, Response
import GetMenu
import uvicorn
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

@app.get("/GetMenusByName")
def GetMenusByName(Name):
    print("Incoming Request:" + Name)
    return {"Menus" : GetMenu.getMenusByName(Name)}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=7000)