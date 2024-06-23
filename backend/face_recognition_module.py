import face_recognition
import ast
import numpy as np
# import matplotlib.pyplot as plt

class FaceRecognitionModule:
    
    @staticmethod
    def image_to_vector(image_path: str) -> str:
        """
        Converts an image to a face vector.
        """
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image, model="large")
        if face_encodings:
            return face_encodings[0].tolist()
        return None

    @staticmethod
    def compare_vectors(vector1: str, vector2: str) -> bool:
        """
        Compares two face vectors and returns True if they belong to the same person.
        """
        encoding1 = np.array(ast.literal_eval(vector1))
        encoding2 = np.array(ast.literal_eval(vector2))
        distance = face_recognition.face_distance([encoding1], encoding2)
        return distance < 0.4
