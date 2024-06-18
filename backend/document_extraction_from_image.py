from dotenv import load_dotenv
from PIL import Image
import requests
import os

load_dotenv()

def get_prediction(image_data):
    prediction_key = os.getenv('AZURE_PREDICTION_KEY')
    prediction_url = os.getenv('AZURE_PREDICTION_URL')

    headers = {
        'Content-Type': 'application/octet-stream',
        'Prediction-Key': prediction_key
    }
    response = requests.post(prediction_url, headers=headers, data=image_data)
    response.raise_for_status()
    return response.json()


def extract_document_from_image(image_path):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    print("dupa 5")
    predictions = get_prediction(image_data)

    image = Image.open(image_path)

    max_probability = 0.0
    best_bbox = None
    print("dupa 2")
    for prediction in predictions['predictions']:
        if prediction['probability'] > max_probability:
            max_probability = prediction['probability']
            best_bbox = prediction['boundingBox']

    padding = 10
    if best_bbox:
        bbox = best_bbox
        left = int(bbox['left'] * image.width)
        top = int(bbox['top'] * image.height)
        width = int(bbox['width'] * image.width)
        height = int(bbox['height'] * image.height)

        expanded_left = max(0, left - padding)
        expanded_top = max(0, top - padding)
        expanded_right = min(image.width, left + width + padding)
        expanded_bottom = min(image.height, top + height + padding)

        cropped_image = image.crop((expanded_left, expanded_top, expanded_right, expanded_bottom))
        print("dupa1")
        return cropped_image
    else:
        print("[Azure Custom Vision] Couldn't find document on image")
    return None