from fastapi import APIRouter, HTTPException
from fastapi import File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
import aiofiles
from face_detector.face_detector import get_face_image, get_face_video
from PIL import Image
import aiofiles
import os
import json
from database.redis import redis_client
from utils.generate_task_id import generate_task_id
router = APIRouter()

# Background task for face detection on image
def process_face_image(task_id, file_path):
    try:
        image = Image.open(file_path)
        result = get_face_image(image)
        redis_client.set(task_id, json.dumps({"status": "completed", "result": result}))
    except Exception as e:
        redis_client.set(task_id, json.dumps({"status": "failed", "error": str(e)}))
    # Remove the file after processing
    finally:
        os.remove(file_path)

# Endpoint to upload an image for face detection
@router.post("/face/image")
async def face_image(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Background task for face detection on video
def process_face_video(task_id, video_path):
    try:
        result = get_face_video(video_path, tasks_id=task_id)
        redis_client.set(task_id, json.dumps({"status": "completed", "result": result}))
    except Exception as e:
        redis_client.set(task_id, json.dumps({"status": "failed", "error": str(e)}))
    finally:
        os.remove(video_path)

# Endpoint to upload a video for face detection
@router.post("/face/video")
async def face_video(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))