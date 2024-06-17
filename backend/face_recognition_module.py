import face_recognition
import numpy as np

class FaceRecognitionModule:
    
    @staticmethod
    def image_to_vector(image_path: str) -> str:
        """
        Converts an image to a face vector.
        """
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        if face_encodings:
            return face_encodings[0].tolist()
        return None

    @staticmethod
    def compare_vectors(vector1: str, vector2: str) -> bool:
        """
        Compares two face vectors and returns True if they belong to the same person.
        """
        encoding1 = np.array(eval(vector1))
        encoding2 = np.array(eval(vector2))
        results = face_recognition.compare_faces([encoding1], encoding2)
        return results[0]
