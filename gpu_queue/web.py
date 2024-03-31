import typing as t
import uvicorn
from pathlib import Path
from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


class GPUList(BaseModel):
    gpus: t.List[str | int]


class ConnectionManager:
    def __init__(self):
        self.active_connections: t.List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)

    async def send(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


class App:
    def __init__(
            self,
            job_submitter: "JobSubmitter",
    ):
        self.app = FastAPI()
        self.connection_manager = ConnectionManager()
        self.job_submitter = job_submitter

        self.register_routes()

    def register_routes(self):
        @self.app.post("/update_gpus")
        async def update_gpus(req: GPUList):
            self.job_submitter.update_available_gpus(req.gpus)

        @self.app.websocket("/ws")
        async def websocket(ws: WebSocket):
            await self.connection_manager.connect(ws)

            try:
                while True:
                    _ = await websocket.receive_text()
            except WebSocketDisconnect:
                self.connection_manager.disconnect(ws)

        self.app.mount("/", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="static")

    async def update_progress(self, job, gpu):
        await self.connection_manager.send({
            "progress": job,
        })

    def launch_server(self, port: int):
        uvicorn.run(self.app, host="0.0.0.0", port=port)
