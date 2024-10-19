from insightface.app import FaceAnalysis
from tqdm import tqdm
import cv2
import numpy as np
from PIL import Image
from database.db import milvus_client
from utils.cv2_to_base64 import cv2_to_base64
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib
from insightface.app import FaceAnalysis
from typing import List,  Optional
from moviepy.editor import VideoFileClip
from sklearn.cluster import OPTICS
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import json
from database.redis import redis_client

matplotlib.use('Agg')

OPTICS_MIN_SAMPLES = 0.02
NUM_DETECTION_FRAME_PER_SECOND = 1

# prepare 'antelopev2' under ./models
app = FaceAnalysis(name='buffalo_l', root='/insightface', providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

def get_face_image(img: Image.Image, max_num: int = 0,task_id=None):

    #outputting html
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    face_info = app.get(img)
    print(len(face_info))
    faces_data = []
    for face in face_info:
        bbox = face['bbox'].astype(int)
        #convert face['embedding'] to list[float]
        embedding_vector = face['embedding'].tolist()
        results = milvus_client.search(collection_name="korean_face",
                                data=[embedding_vector],
                                search_params={"params":{'range_filter':0.7,
                                                            'radius':0.35,
                                                            }},
                                output_fields=['name', 'img_url','description','detail_url','data_source','img_path'],
                                limit=10,)
        if len(results[0])>0:
            result_data = results[0][0]['entity']
        else:
            result_data = {
                'name': 'Unknown',
                'img_url': 'https://www.pngitem.com/pimgs/m/146-1468479_my-profile-icon-blank-profile-picture-circle-hd.png',
                'description': 'Unknown',
                'detail_url': 'https://www.google.com',
            }
        cropped_face = img[max(0, bbox[1]):min(bbox[3], img.shape[0]), max(0, bbox[0]):min(bbox[2], img.shape[1])]
        result_data['bbox'] ={
            'x_min': bbox[0] / img.shape[1],
            'y_min': bbox[1] / img.shape[0],
            'x_max': bbox[2] / img.shape[1],
            'y_max': bbox[3] / img.shape[0],
        }
        #convert to html b64 image string
        b64_face = cv2_to_base64(cropped_face)
        faces_data.append({
            'b64_face': b64_face,
            **result_data
        })

    '''
    html_string = """
    <table border="1">
        <tr>
            <th>Original Face</th>
            <th>Matched Face</th>
            <th>Name</th>
            <th>Description</th>
            <th>More Info</th>
        </tr>
    """
    for face_data in faces_data:
        html_string += f"""
        <tr>
            <td><img src='data:image/jpeg;base64,{face_data['b64_face']}' width='250'/></td>
            <td><img src='{face_data['img_url']}' width='250'/></td>
            <td>{face_data['name']}</td>
            <td>{face_data['description']}</td>
            <td><a href='{face_data['detail_url']}' target='_blank'>More Info</a></td>
        </tr>
        """
    html_string += "</table>"
    '''
    return faces_data

class CharacterBoundingBox():
    def __init__(self, embedding_vector: List[float], start_frame:int,cluster_id:Optional[int]=None):
        self.embedding_vector = embedding_vector
        self.cluster_id = cluster_id
        self.start_frame = start_frame
        self.end_frame = start_frame
        self.box_frames = {}
    def to_dict(self):
        for key, value in self.box_frames.items():
            #print(key, value)
            self.box_frames[key] = list(value)
        return {'embedding_vector': self.embedding_vector,
                'start_frame': self.start_frame, 
                'end_frame': self.end_frame, 
                'box_frames': self.box_frames}
    
def get_face_video(input_video_path: str, plot_pca=True,tasks_id=None):
    """
    Processes a video to detect faces, perform clustering, and generate an HTML string with the results.

    Args:
        input_video_path (str): The path to the input video file.
        plot_pca (bool, optional): Whether to plot PCA results. Defaults to True.

    Returns:
        str: An HTML string containing the face detection and clustering results.
    """
    clip, fps, frame_count, duration, width, height = load_video(input_video_path)
    list_all_character_bounding_box, list_active_character_bounding_box = process_frames(clip, fps, frame_count,tasks_id)
    list_all_character_bounding_box_dict = convert_to_dict(list_all_character_bounding_box)
    redis_client.set(tasks_id, json.dumps({"status": "performing clustering"}))
    clusters, X_pca = perform_clustering(list_all_character_bounding_box_dict)
    redis_client.set(tasks_id, json.dumps({"status": "generating faces data"}))
    faces_data = generate_faces_data(clip, fps, list_all_character_bounding_box_dict, clusters)
    data = generate_json(faces_data, plot_pca, X_pca, clusters)
    clip.reader.close()
    return data

def load_video(input_video_path: str):
    """
    Loads a video file and extracts its properties.

    Args:
        input_video_path (str): The path to the input video file.

    Returns:
        tuple: A tuple containing the following elements:
            - clip (VideoFileClip): The loaded video clip.
            - fps (float): The frames per second of the video.
            - frame_count (int): The total number of frames in the video.
            - duration (int): The duration of the video in seconds.
            - width (int): The width of the video in pixels.
            - height (int): The height of the video in pixels.
    """
    clip = VideoFileClip(input_video_path)
    fps = clip.fps
    frame_count = int(clip.fps * clip.duration)
    duration = int(clip.duration)
    width = int(clip.size[0])
    height = int(clip.size[1])
    print(f"fps: {fps}, frame_count: {frame_count}, duration: {duration}, width: {width}, height: {height}")
    return clip, fps, frame_count, duration, width, height

def process_frames(clip, fps, frame_count,tasks_id=None):
    """
    Processes frames from a video clip to detect faces and update bounding boxes.

    Args:
        clip (VideoFileClip): The video clip to process.
        fps (int): Frames per second of the video.
        frame_count (int): Total number of frames in the video.
        tasks_id (str): The task ID for the video processing task.

    Returns:
        tuple: A tuple containing:
            - list_all_character_bounding_box (list): A list of all detected character bounding boxes.
            - list_active_character_bounding_box (list): A list of currently active character bounding boxes.
    """
    list_all_character_bounding_box = []
    list_active_character_bounding_box = []
    counter =0
    for i in (pbar := tqdm(range(0, frame_count, int(fps / NUM_DETECTION_FRAME_PER_SECOND)))):
        counter += int(fps / NUM_DETECTION_FRAME_PER_SECOND)
        if counter % (5 * int(fps / NUM_DETECTION_FRAME_PER_SECOND)) == 0 and tasks_id:
            redis_client.set(tasks_id, json.dumps({"status": f"processing {counter}/{frame_count} frames"}))
        ret, frame = True, clip.get_frame(i / fps)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if ret:
            face_info = app.get(frame)
            process_faces(face_info, i, fps, list_active_character_bounding_box)
            update_bounding_boxes(i, fps, list_active_character_bounding_box, list_all_character_bounding_box)
            pbar.set_description(f"Active Bounding Box: {len(list_active_character_bounding_box)}, All Bounding Box: {len(list_all_character_bounding_box)}")
        else:
            print("Video ended")
    list_all_character_bounding_box.extend(list_active_character_bounding_box)
    return list_all_character_bounding_box, list_active_character_bounding_box

def process_faces(face_info, frame_index, fps, list_active_character_bounding_box):
    """
    Processes detected faces and updates the list of active character bounding boxes.

    Args:
        face_info (list): A list of dictionaries containing face information. Each dictionary should have keys 'bbox' 
                          (bounding box as a numpy array) and 'embedding' (embedding vector as a numpy array).
        frame_index (int): The current frame index.
        fps (int): Frames per second of the video.
        list_active_character_bounding_box (list): A list of CharacterBoundingBox objects representing active characters 
                                                   in the video.

    Returns:
        None
    """
    for face in face_info:
        bbox = face['bbox'].astype(int)
        embedding_vector = face['embedding'].tolist()
        encountered_previous_frame = False
        for active_character_bounding_box in list_active_character_bounding_box:
            if active_character_bounding_box.start_frame >= frame_index:
                continue
        if not encountered_previous_frame:
            list_active_character_bounding_box.append(CharacterBoundingBox(embedding_vector=embedding_vector, start_frame=frame_index))
            list_active_character_bounding_box[-1].box_frames[frame_index] = bbox

def update_bounding_boxes(frame_index, fps, list_active_character_bounding_box, list_all_character_bounding_box):
    """
    Updates the list of active character bounding boxes by moving expired or long-lived bounding boxes 
    to the list of all character bounding boxes.

    Parameters:
    frame_index (int): The current frame index.
    fps (int): Frames per second of the video.
    list_active_character_bounding_box (list): List of currently active character bounding boxes.
    list_all_character_bounding_box (list): List of all character bounding boxes.

    Returns:
    None
    """
    to_remove = []
    for active_character_bounding_box in list_active_character_bounding_box:
        if active_character_bounding_box.end_frame <= frame_index or active_character_bounding_box.end_frame - active_character_bounding_box.start_frame >= 10:
            list_all_character_bounding_box.append(active_character_bounding_box)
            to_remove.append(active_character_bounding_box)
    for active_character_bounding_box in to_remove:
        list_active_character_bounding_box.remove(active_character_bounding_box)

def convert_to_dict(list_all_character_bounding_box):
    """
    Converts a list of character bounding box objects to a list of dictionaries.

    Args:
        list_all_character_bounding_box (list): A list of character bounding box objects, 
                                                each having a `to_dict` method that converts 
                                                the object to a dictionary.

    Returns:
        list: A list of dictionaries where each dictionary represents a character bounding box.
              The 'box_frames' key in each dictionary is processed to convert its keys to integers 
              and its values to lists, and then sorted by the integer keys.
    """
    list_all_character_bounding_box_dict = [character_bounding_box.to_dict() for character_bounding_box in list_all_character_bounding_box]
    for character_bounding_box in list_all_character_bounding_box_dict:
        for key, value in character_bounding_box['box_frames'].items():
            character_bounding_box['box_frames'][int(key)] = list(value)
        character_bounding_box['box_frames'] = dict(sorted(character_bounding_box['box_frames'].items()))
    return list_all_character_bounding_box_dict

def perform_clustering(list_all_character_bounding_box_dict):
    """
    Perform clustering on a list of character bounding box dictionaries.

    This function takes a list of dictionaries, each containing an 'embedding_vector' key,
    and performs clustering using PCA for dimensionality reduction and OPTICS for clustering.

    Args:
        list_all_character_bounding_box_dict (list): A list of dictionaries, where each dictionary
                                                     contains an 'embedding_vector' key.

    Returns:
        tuple: A tuple containing:
            - clusters (numpy.ndarray): An array of cluster labels for each character bounding box.
            - X_pca (numpy.ndarray): The PCA-transformed and standardized embedding vectors.
    """
    embedding_vector = [character_bounding_box['embedding_vector'] for character_bounding_box in list_all_character_bounding_box_dict]
    X = np.array(embedding_vector)
    X = X / np.linalg.norm(X, axis=1)[:, None]
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    X_pca = StandardScaler().fit_transform(X_pca)
    db = OPTICS(min_cluster_size=OPTICS_MIN_SAMPLES).fit(X_pca)
    clusters = db.labels_
    print(clusters)
    for character_bounding_box, cluster_id in zip(list_all_character_bounding_box_dict, clusters):
        character_bounding_box['cluster_id'] = cluster_id
    return clusters, X_pca

def generate_faces_data(clip, fps, list_all_character_bounding_box_dict, clusters):
    """
    Generate face data for characters in a video clip.

    Args:
        clip (VideoFileClip): The video clip from which to extract frames.
        fps (int): Frames per second of the video clip.
        list_all_character_bounding_box_dict (dict): Dictionary containing bounding box information for all characters.
        clusters (list): List of cluster labels for the characters.

    Returns:
        list: A list of dictionaries containing base64 encoded face images and additional result data.
    """
    labels = [label for label in list(set(clusters)) if label != -1]
    faces_data = []
    for idx, cluster in enumerate(labels):
        character_bounding_box = get_largest_bounding_box(list_all_character_bounding_box_dict, cluster)
        start_frame = character_bounding_box['start_frame']
        box_frame = character_bounding_box['box_frames'][start_frame]
        embedding_vector = character_bounding_box['embedding_vector']
        results = milvus_client.search(collection_name="korean_face",
                                       data=[embedding_vector],
                                       search_params={"params": {'range_filter': 0.8, 'radius': 0.35}},
                                       output_fields=['name', 'img_url', 'description', 'detail_url', 'data_source', 'img_path'],
                                       limit=10,)
        result_data = get_result_data(results)
        result_data['bbox'] ={
            'x_min': box_frame[0] / clip.size[0],
            'y_min': box_frame[1] / clip.size[1],
            'x_max': box_frame[2] / clip.size[0],
            'y_max': box_frame[3] / clip.size[1],
        }
        frame = clip.get_frame(start_frame / fps)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cropped_face = frame[max(0, box_frame[1]):min(box_frame[3], frame.shape[0]), max(0, box_frame[0]):min(box_frame[2], frame.shape[1])]
        b64_face = cv2_to_base64(cropped_face) if cropped_face.shape[0] != 0 and cropped_face.shape[1] != 0 else "data:image/jpeg;base64,"
        faces_data.append({'b64_face': b64_face, **result_data})
    return faces_data

def get_largest_bounding_box(list_all_character_bounding_box_dict, cluster):
    """
    Finds and returns the character bounding box with the largest area for a given cluster.

    Args:
        list_all_character_bounding_box_dict (list): A list of dictionaries, where each dictionary contains 
            information about a character's bounding box, including 'cluster_id', 'box_frames', and 'start_frame'.
        cluster (int): The cluster ID to filter the bounding boxes.

    Returns:
        dict: The dictionary representing the character bounding box with the largest area within the specified cluster.
    """
    max_bbox_area = 0
    character_bounding_box = {}
    for character_bounding_box_ in list_all_character_bounding_box_dict:
        if character_bounding_box_['cluster_id'] == cluster:
            bbox_area = (character_bounding_box_['box_frames'][character_bounding_box_['start_frame']][2] - character_bounding_box_['box_frames'][character_bounding_box_['start_frame']][0]) * (character_bounding_box_['box_frames'][character_bounding_box_['start_frame']][3] - character_bounding_box_['box_frames'][character_bounding_box_['start_frame']][1])
            if bbox_area > max_bbox_area:
                max_bbox_area = bbox_area
                character_bounding_box = character_bounding_box_
    character_bounding_box['embedding_vector']  = np.mean([ character_bounding_box_['embedding_vector'] for character_bounding_box_ in list_all_character_bounding_box_dict if character_bounding_box_['cluster_id'] == cluster], axis=0)
    return character_bounding_box

def get_result_data(results):
    """
    Extracts the entity data from the results if available, otherwise returns a default 'Unknown' entity.

    Args:
        results (list): A list of results where each result is expected to be a list of dictionaries containing entity data.

    Returns:
        dict: A dictionary containing entity data. If no similar face is found, returns a default dictionary with 'Unknown' entity information.
    """
    if len(results[0]) > 0:
        return results[0][0]['entity']
    else:
        print("No similar face found")
        return {
            'name': 'Unknown',
            'img_url': 'https://www.pngitem.com/pimgs/m/146-1468479_my-profile-icon-blank-profile-picture-circle-hd.png',
            'description': 'Unknown',
            'detail_url': 'https://www.google.com',
        }

def generate_json(faces_data, plot_pca, X_pca, clusters):
    """
    Generates an JSON containing face data and optionally a PCA plot.

    Args:
        faces_data (list of dict): A list of dictionaries where each dictionary contains:
            - 'b64_face' (str): Base64 encoded string of the original face image.
            - 'img_url' (str): URL of the matched face image.
            - 'name' (str): Name associated with the face.
            - 'description' (str): Description of the face.
            - 'detail_url' (str): URL for more information about the face.
        plot_pca (bool): If True, includes a PCA plot in the HTML.
        X_pca (numpy.ndarray): PCA-transformed data points.
        clusters (numpy.ndarray): Cluster labels for the data points.

    Returns:
        dict : A dictionary containing the face data and optionally a PCA plot.
    """
    '''
    html_string = """
    <table border="1">
        <tr>
            <th>Original Face</th>
            <th>Matched Face</th>
            <th>Name</th>
            <th>Description</th>
            <th>More Info</th>
        </tr>
    """
    for face_data in faces_data:
        html_string += f"""
        <tr>
            <td><img src='data:image/jpeg;base64,{face_data['b64_face']}' width='250'/></td>
            <td><img src='{face_data['img_url']}' width='250'/></td>
            <td>{face_data['name']}</td>
            <td>{face_data['description']}</td>
            <td><a href='{face_data['detail_url']}' target='_blank'>More Info</a></td>
        </tr>
        """
    html_string += "</table>"
    '''

    if plot_pca:
        fig, ax = plt.subplots()
        labels = [label for label in list(set(clusters)) if label != -1]
        for face_data, label in zip(faces_data, labels):
            ax.scatter(X_pca[clusters == label, 0], X_pca[clusters == label, 1], label=label)
            ax.annotate(face_data['name'], (np.mean(X_pca[clusters == label, 0]), np.mean(X_pca[clusters == label, 1])))
        fig.canvas.draw()
        img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        b64_plot = cv2_to_base64(img)
        #html_string += f"<img src='data:image/jpeg;base64,{b64_plot}' width='100%'/>"
        plt.close(fig)

    return_data = {
        'faces_data': faces_data,
        'plot_pca': b64_plot if plot_pca else None
    }
    return return_data
    
    