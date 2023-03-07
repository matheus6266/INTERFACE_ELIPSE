from fastapi import FastAPI, Request
from typing import Any, Dict, List, Union
import json
from pydantic import BaseModel


class Item(BaseModel):
    data1: Union[float,None] = None
    data2: Union[float,None] = None



app= FastAPI()

@app.get("/gg")
def gg():
    return "{\"ok\":1}"



@app.post("/operationloadcell")
async def handle(item: Item):
    
    resposta={
        "data3":(item.data1)+10,
        "data4":(item.data2)+20
    }
    return resposta

@app.post("/Operation_LoadCellCalibration")
async def handle(info: Request):
    req_info= await info.json()
    print(req_info)
    resposta={
        "recebido":req_info
    }
    return resposta