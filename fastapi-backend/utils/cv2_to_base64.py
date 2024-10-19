

import base64
from io import BytesIO
import cv2
from PIL import Image

def cv2_to_base64(img_np_array):
    try:
        # Convert OpenCV image (BGR format) to RGB format
        img_rgb = cv2.cvtColor(img_np_array, cv2.COLOR_BGR2RGB)

        # Convert RGB image to PIL Image for easier encoding
        pil_img = Image.fromarray(img_rgb)

        # Save the PIL Image to a BytesIO object
        buffered = BytesIO()
        pil_img.save(buffered, format="JPEG")  # You can use "PNG" if preferred

        # Encode image to base64
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return f"data:image/jpeg;base64,{img_base64}"
    except Exception as e:
        return f"data:image/jpeg;base64,"
