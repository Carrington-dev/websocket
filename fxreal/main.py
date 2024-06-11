import asyncio
from fastapi import FastAPI, WebSocket, Depends, HTTPException, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import websockets

app = FastAPI()

class Message(BaseModel):
    message: str 



html = """
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI WebSocket</title>
    </head>
    <body>
        <h1>WebSocket Test</h1>
        <button onclick="sendMessage()">Send Message</button>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");

            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };

            function sendMessage() {
                ws.send("Hello WebSocket")
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Carrington, Message text was: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")


# Define a dependency function to get the WebSocket connection
async def get_websocket(websocket: WebSocket) -> WebSocket:
    try:
        # Accept the WebSocket connection
        await websocket.accept()
        return websocket
    except WebSocketDisconnect:
        raise HTTPException(status_code=400, detail="WebSocket connection closed")

async def send_data(message):
    # websocket = WebSocket()
    websocket: WebSocket = WebSocket(port=8000)
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"From API, Message text was: {message}")
    except WebSocketDisconnect:
        print("Client disconnected")


import asyncio

async def my_coroutine():
    print("Coroutine is starting...")
    await asyncio.sleep(1)  # Simulate some asynchronous operation
    print("Coroutine is done!")

async def master():
    print("Main is starting...")
    await my_coroutine()
    print("Main is done!")

# Run the event loop
# asyncio.run(main())

    


# @app.post("/messages")
# # @app.websocket("/ws")
# def send_data_to_websocket(message: Message, websocket: WebSocket):
#     asyncio.run(send_data(message=message.message, websocket=websocket))
#     return message

@app.post("/messages")
async def process_data(message: Message):
    data = message.message
    # Assuming you want to send received data over WebSocket
    try:
        # await send_data(message=message.message)
        asyncio.run(master)
        return message
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send data over WebSocket")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
