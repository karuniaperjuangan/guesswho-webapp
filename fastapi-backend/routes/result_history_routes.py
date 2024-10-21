from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Response
from models.user import User
from models.result_history import ResultHistory, ResultHistoryRequest,RecognitionResult, CreateResultHistoryRequest
from pymongo.collection import Collection
from database.mongo import get_current_user, get_result_history_collection
router = APIRouter()

@router.get("/user/list_history")
def get_all_result_history(user: Annotated[User, Depends(get_current_user)], result_history_collection: Annotated[Collection, Depends(get_result_history_collection)]):
    try:
        results = list(result_history_collection.find({"username": user.username}))
        for item in results:
            item["_id"] = str(item["_id"])
        return results
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/history")
def get_result_history_by_name(user: Annotated[User, Depends(get_current_user)], history_name:str, result_history_collection: Annotated[Collection, Depends(get_result_history_collection)]):
    try:
        result = result_history_collection.find_one({"username": user.username, "history_name": history_name})
        if not result:
            raise HTTPException(status_code=404, detail="Result history not found")
        print(result)
        result["_id"] = str(result["_id"])
        return result
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.post("/user/history")
def create_result_history(user: Annotated[User, Depends(get_current_user)], request: CreateResultHistoryRequest, result_history_collection: Annotated[Collection, Depends(get_result_history_collection)]):
    try:
        if result_history_collection.find_one({"username": user.username, "history_name": request.history_name}):
            raise HTTPException(status_code=409, detail="Result history already exists")
        recognition_result = request.recognition_result
        # Create a new document with the recognition result
        new_document = {
            "username": user.username,
            "history_name": request.history_name,
            "b64_media": request.b64_media,
            "recognition_result": recognition_result.model_dump()
        }
        # Insert the new document into the collection
        result_history_collection.insert_one(new_document)
        new_document["_id"] = str(new_document["_id"])
        # Return the created document as a response
        print(new_document)
        return new_document
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/user/history", status_code=204)
def delete_result_history(user: Annotated[User, Depends(get_current_user)], request: ResultHistoryRequest, result_history_collection: Annotated[Collection, Depends(get_result_history_collection)]):
    try:
        # Find the document with the specified username and history name
        document = result_history_collection.find_one({"username": user.username, "history_name": request.history_name})
        if not document:
            raise HTTPException(status_code=404, detail="Result history not found")
        # Delete the document from the collection
        result_history_collection.delete_one(document)
        # Return a 204 No Content response
        return Response(status_code=204)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))