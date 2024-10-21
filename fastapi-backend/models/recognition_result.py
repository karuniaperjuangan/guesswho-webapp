from typing import List
from pydantic import BaseModel


class Bbox(BaseModel):
    x_min: float
    y_min: float
    x_max: float
    y_max: float


class Face(BaseModel):
    b64_face: str
    name: str
    img_url: str
    description: str
    detail_url: str
    data_source: str
    img_path: str
    bbox: Bbox


class RecognitionResult(BaseModel):
    result: List[Face]

class RecognitionResultHistory(BaseModel):
    username : str
    name : str
    recognition_result : RecognitionResult
