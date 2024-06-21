import asyncio
from datetime import datetime
from json import dumps
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from src import Finance, ConnectionManager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()

templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    USDtoEUR: "float" = Finance().generate(firstCurrency="USD", secondCurrency="EUR")
    EURtoGBP: "float" = Finance().generate(firstCurrency="EUR", secondCurrency="GBP")
    GBPtoUSD: "float" = Finance().generate(firstCurrency="GBP", secondCurrency="USD")
    time: "str" = str(datetime.now())

items = dict()

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    context = dict()
    context["request"] = request
    context["name"] = "FxTools"
    context["title"] = "FxTools"
    return templates.TemplateResponse("index.html", context)

@app.get("/update", response_class=HTMLResponse)
async def read_item(request: Request):
    context = dict()
    context["request"] = request
    context["name"] = "FxTools"
    context["title"] = "FxTools"
    return templates.TemplateResponse("forex.html", context)



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(1)  # simulate periodic updates
        # USD to EUR: 0.85
        # EUR to GBP: 0.75
        # GBP to USD: 1.20
        context =  dict()
        # 
        if(len(items) > 0):
            items['USDtoEUR'] = Finance().generate(firstCurrency="USD", secondCurrency="EUR")
            items['EURtoGBP'] = Finance().generate(firstCurrency="EUR", secondCurrency="GBP")
            items['GBPtoUSD'] = Finance().generate(firstCurrency="GBP", secondCurrency="USD")
            items['time'] = str(datetime.now())

            await websocket.send_text(dumps(items))
        else:
            context['USDtoEUR'] = Finance().generate(firstCurrency="USD", secondCurrency="EUR")
            context['EURtoGBP'] = Finance().generate(firstCurrency="EUR", secondCurrency="GBP")
            context['GBPtoUSD'] = Finance().generate(firstCurrency="GBP", secondCurrency="USD")
            context['time'] = str(datetime.now())
            print(str(datetime.now()))
            
            await websocket.send_text(dumps(context))

@app.websocket("/ws/create")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keeping connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/forex/")
async def create_forex(item: Item):
    items = item
    await manager.broadcast(dumps({**item.model_dump()}))
    return items

@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            return await websocket.receive_text()  # Keeping connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.put("/forex/")
async def update_forex(item: Item):
    items = item
    await manager.broadcast(dumps({**item.model_dump()}))
    return items

    

