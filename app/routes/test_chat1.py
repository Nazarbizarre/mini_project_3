import asyncio
import websockets


async def main(room_id: int):
    async with websockets.connect(f"ws://localhost:8000/ws/{room_id}") as ws:
        await ws.send("Hello bro")
        message = await ws.recv()
        print(f"Received: {message}")


asyncio.run(main(1))