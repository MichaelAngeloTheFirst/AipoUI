import unittest
from face_recognition_module import FaceRecognitionModule

class TestFaceRecognitionModule(unittest.TestCase):
    def setUp(self):
        # Sample test data: Paths to images for testing
        self.image_path_1 = "test_resources/gb1.jpg"
        self.image_path_2 = "test_resources/gb2.jpg"
        self.image_path_3 = "test_resources/gb3.jpg"
        self.image_path_4 = "test_resources/dt.jpg"
        self.image_path_5 = "test_resources/amz.jpg"
        
        # Generate face vectors for test images
        self.vector1 = FaceRecognitionModule.image_to_vector(self.image_path_1)
        self.vector2 = FaceRecognitionModule.image_to_vector(self.image_path_2)
        self.vector3 = FaceRecognitionModule.image_to_vector(self.image_path_3)
        self.vector4 = FaceRecognitionModule.image_to_vector(self.image_path_4)
        self.vector5 = FaceRecognitionModule.image_to_vector(self.image_path_5)

    def test_image_to_vector(self):
        # Test if the face vectors are not None
        self.assertIsNotNone(self.vector1, "Face vector for image1 should not be None")
        self.assertIsNotNone(self.vector2, "Face vector for image2 should not be None")
        self.assertIsNotNone(self.vector3, "Face vector for image3 should not be None")
        self.assertIsNotNone(self.vector4, "Face vector for image4 should not be None")
        self.assertIsNotNone(self.vector5, "Face vector for image5 should not be None")

    def test_compare_vectors_same_person_1(self):
        # Test if two face vectors of the same person are recognized as the same
        self.assertTrue(FaceRecognitionModule.compare_vectors(str(self.vector1), str(self.vector2)),
                        "Face vectors for image1 and image2 should be recognized as the same")
        
    def test_compare_vectors_same_person_2(self):
        # Test if two face vectors of the same person are recognized as the same
        self.assertTrue(FaceRecognitionModule.compare_vectors(str(self.vector1), str(self.vector3)),
                        "Face vectors for image1 and image3 should be recognized as the same")
        
    def test_compare_vectors_same_person_3(self):
        # Test if two face vectors of the same person are recognized as the same
        self.assertTrue(FaceRecognitionModule.compare_vectors(str(self.vector2), str(self.vector3)),
                        "Face vectors for image2 and image3 should be recognized as the same")

    def test_compare_vectors_different_person(self):
        # Test if two face vectors of different people are recognized as different
        self.assertFalse(FaceRecognitionModule.compare_vectors(str(self.vector1), str(self.vector4)),
                         "Face vectors for image1 and image4 should be recognized as different")

    def test_compare_vectors_another_different_person(self):
        # Test another pair of different people
        self.assertFalse(FaceRecognitionModule.compare_vectors(str(self.vector4), str(self.vector5)),
                         "Face vectors for image4 and image5 should be recognized as different")

    def test_image_to_vector_no_face(self):
        # Test with an image that does not contain a face
        image_path_no_face = "test_resources/no_face.jpg"
        vector_no_face = FaceRecognitionModule.image_to_vector(image_path_no_face)
        self.assertIsNone(vector_no_face, "Face vector for image without face should be None")

    def test_compare_vectors_same_image(self):
        # Test if the same image is recognized as the same
        self.assertTrue(FaceRecognitionModule.compare_vectors(str(self.vector1), str(self.vector1)),
                        "The same image vector should be recognized as the same")

if __name__ == '__main__':
    unittest.main()
