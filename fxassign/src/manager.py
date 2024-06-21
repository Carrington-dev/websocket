from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware



# Manager for handling WebSocket connections and broadcasting messages
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def recieve_message(self, websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                await websocket.receive_text()  # Keeping connection alive
        except WebSocketDisconnect:
           pass


    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

