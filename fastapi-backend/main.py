from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import aiofiles
import os
import json
from database.redis import redis_client
import dotenv
from routes.face_routes import router as face_router
from routes.authetication_routes import router as auth_router
dotenv.load_dotenv()

# Initialize FastAPI app and Redis client
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(face_router)
app.include_router(auth_router)
@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Endpoint to check the status of a task
@app.get("/task/status/{task_id}")
async def task_status(task_id: str):
    task_data = redis_client.get(task_id)
    if task_data is None:
        return JSONResponse(content={"error": "Task not found"}, status_code=404)

    # Return the task status and result if completed
    return JSONResponse(content=json.loads(task_data))

@app.get("/client")
async def read_client():
    html_path = os.path.join(os.path.dirname(__file__), "client", "index.html")
    async with aiofiles.open(html_path, mode="r") as f:
        content = await f.read()
        return HTMLResponse(content=content)