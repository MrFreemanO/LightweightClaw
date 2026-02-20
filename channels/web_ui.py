from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
import uvicorn
import json

app = FastAPI()
agent_instance = None

@app.get("/")
async def get():
    return FileResponse("static/index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            msg = payload.get("message", "")
            persona = payload.get("persona", "mira")
            
            # Отправка запроса в ядро агента
            reply = await agent_instance.process(msg, persona)
            
            await websocket.send_json({"text": reply})
        except Exception as e:
            print(f"WS Error: {e}")
            break

async def start_web_ui(agent):
    global agent_instance
    agent_instance = agent
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    print("🌐 Web UI запущен на http://localhost:8000")
    await server.serve()
