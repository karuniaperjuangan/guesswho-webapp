from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import aiofiles
from face_detector.face_detector import get_face_image, get_face_video
from PIL import Image
import aiofiles
import os
import uuid
import json
from database.redis import redis_client

# Initialize FastAPI app and Redis client
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to generate a unique task ID
def generate_task_id():
    return str(uuid.uuid4())

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Background task for face detection on image
def process_face_image(task_id, file_path):
    image = Image.open(file_path)
    result = get_face_image(image)
    redis_client.set(task_id, json.dumps({"status": "completed", "result": result}))
    os.remove(file_path)

# Endpoint to upload an image for face detection
@app.post("/face/image")
async def face_image(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    task_id = generate_task_id()
    file_path = f"/tmp/{task_id}.png"

    # Save the uploaded image file
    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    # Set initial task status in Redis and launch background task
    redis_client.set(task_id, json.dumps({"status": "processing"}))
    background_tasks.add_task(process_face_image, task_id, file_path)

    return JSONResponse(content={"task_id": task_id, "status": "processing"})

# Background task for face detection on video
def process_face_video(task_id, video_path):
    result = get_face_video(video_path, tasks_id=task_id)
    redis_client.set(task_id, json.dumps({"status": "completed", "result": result}))
    os.remove(video_path)

# Endpoint to upload a video for face detection
@app.post("/face/video")
async def face_video(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    task_id = generate_task_id()
    video_path = f"/tmp/{task_id}.mp4"

    # Save the uploaded video file
    async with aiofiles.open(video_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    # Set initial task status in Redis and launch background task
    redis_client.set(task_id, json.dumps({"status": "processing"}))
    background_tasks.add_task(process_face_video, task_id, video_path)

    return JSONResponse(content={"task_id": task_id, "status": "processing"})

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