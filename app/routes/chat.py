from typing import Annotated, List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status, WebSocket, WebSocketDisconnect
from sqlalchemy import select, update


from ..schemas import Advertisement, UpdateItemSchema, ItemResponse
from ..db import AsyncDB, Item, User
from ..utils import get_current_user
from .. import app




class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: int):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: int):
        if room_id in self.active_connections:
            self.active_connections.get(room_id).remove(websocket)

    async def broadcast(self, room_id: int, message: dict):
        for connection in self.active_connections.get(room_id):
            await connection.send_text(message)
            
connection_manager = ConnectionManager()

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(room_id: int, websocket: WebSocket):
    await connection_manager.connect(websocket, int(room_id))

    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            await connection_manager.broadcast(room_id, data)

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, room_id)
        await connection_manager.broadcast(room_id, "User left the Chat")
