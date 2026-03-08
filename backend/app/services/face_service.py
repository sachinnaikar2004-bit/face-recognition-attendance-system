"""
Face recognition service for business logic operations.
"""

import cv2
import numpy as np
from deepface import DeepFace
from typing import List, Optional, Tuple, Dict, Any
import base64
import io
from PIL import Image

from app.models.employee_model import Employee
from app.core.exceptions import FaceRecognitionException, ValidationException
from app.core.config import settings
from app.services.employee_service import EmployeeService


class FaceService:
    """Service for face recognition operations."""
    
    def __init__(self):
        self.employee_service = EmployeeService()
        self.known_face_encodings = []
        self.known_employee_ids = []
    
    async def recognize_face(self, image_data: str) -> Optional[Employee]:
        """Recognize face from image data and return matching employee."""
        try:
            # Decode base64 image
            image = self._decode_base64_image(image_data)
            
            # Detect faces in the image using DeepFace
            try:
                # Convert to RGB for DeepFace
                if len(image.shape) == 3:
                    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                else:
                    rgb_image = image
                
                # Get face embeddings
                embedding_objs = DeepFace.represent(
                    rgb_image,
                    enforce_detection=True,
                    detector_backend='opencv',
                    model_name='VGG-Face'
                )
                
                if not embedding_objs:
                    raise FaceRecognitionException("No face detected in the image")
                
                face_embeddings = [np.array(obj['embedding']) for obj in embedding_objs]
                
            except Exception as e:
                if "Face could not be detected" in str(e):
                    raise FaceRecognitionException("No face detected in the image")
                else:
                    raise FaceRecognitionException(f"Face detection failed: {str(e)}")
            
            # Load known face encodings from database
            await self._load_known_face_encodings()
            
            if not self.known_face_encodings:
                raise FaceRecognitionException("No registered faces found in database")
            
            # Compare each detected face with known faces
            for face_embedding in face_embeddings:
                best_match_id, confidence = self._find_best_match(face_embedding)
                
                if best_match_id and confidence >= (1 - settings.deepface_tolerance):
                    employee = await self.employee_service.get_employee_by_id(best_match_id)
                    return employee
            
            return None
            
        except FaceRecognitionException:
            raise
        except Exception as e:
            raise FaceRecognitionException(f"Face recognition failed: {str(e)}")
    
    async def register_face(self, emp_id: str, face_images: List[str]) -> Dict[str, Any]:
        """Register face for employee."""
        try:
            employee = await self.employee_service.get_employee_by_id(emp_id)
            if not employee:
                raise ValidationException("Employee not found")
            
            face_encodings = []
            
            for i, image_data in enumerate(face_images):
                # Decode and validate image
                image = self._decode_base64_image(image_data)
                quality_score = self._assess_image_quality(image)
                
                if quality_score < settings.image_quality_threshold:
                    raise ValidationException(f"Image {i+1} quality too low: {quality_score:.2f}")
                
                # Generate face embedding using DeepFace
                try:
                    # Convert to RGB for DeepFace
                    if len(image.shape) == 3:
                        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    else:
                        rgb_image = image
                    
                    # Get face embedding
                    embedding_objs = DeepFace.represent(
                        rgb_image,
                        enforce_detection=True,
                        detector_backend='opencv',
                        model_name='VGG-Face'
                    )
                    
                    if len(embedding_objs) != 1:
                        raise ValidationException(f"Image {i+1} must contain exactly one face")
                    
                    face_encoding = np.array(embedding_objs[0]['embedding'])
                    face_encodings.append(face_encoding)
                    
                except Exception as e:
                    if "Face could not be detected" in str(e):
                        raise ValidationException(f"No face detected in image {i+1}")
                    else:
                        raise ValidationException(f"Could not generate face embedding from image {i+1}: {str(e)}")
            
            # Average multiple encodings for better accuracy
            averaged_encoding = self._average_encodings(face_encodings)
            
            # Update employee face encoding
            employee.face_encoding = averaged_encoding.tolist()
            await self.employee_service.update_employee(emp_id, {"face_encoding": employee.face_encoding})
            
            return {
                "success": True,
                "message": f"Successfully registered {len(face_images)} face images",
                "quality_scores": [self._assess_image_quality(self._decode_base64_image(img)) for img in face_images]
            }
            
        except ValidationException:
            raise
        except Exception as e:
            raise FaceRecognitionException(f"Face registration failed: {str(e)}")
    
    async def detect_faces(self, image_data: str) -> Dict[str, Any]:
        """Detect faces in image."""
        try:
            image = self._decode_base64_image(image_data)
            
            # Detect faces using DeepFace
            try:
                # Convert to RGB for DeepFace
                if len(image.shape) == 3:
                    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                else:
                    rgb_image = image
                
                # Get face detections
                face_objs = DeepFace.analyze(
                    rgb_image,
                    actions=['age', 'gender', 'emotion'],
                    enforce_detection=False,
                    detector_backend='opencv'
                )
                
                if not face_objs:
                    return {
                        "faces_detected": 0,
                        "faces": []
                    }
                
                # Prepare detection info
                detections = []
                for face_obj in face_objs:
                    if 'region' in face_obj:
                        region = face_obj['region']
                        x, y, w, h = region['x'], region['y'], region['w'], region['h']
                        
                        detection = {
                            "x": int(x),
                            "y": int(y),
                            "width": int(w),
                            "height": int(h),
                            "confidence": face_obj.get('confidence', 0.0),
                            "age": face_obj.get('age', 0),
                            "gender": face_obj.get('dominant_gender', 'unknown'),
                            "emotion": face_obj.get('dominant_emotion', 'unknown')
                        }
                        detections.append(detection)
                
                return {
                    "faces_detected": len(detections),
                    "faces": detections
                }
                
            except Exception:
                return {
                    "faces_detected": 0,
                    "faces": []
                }
            
        except Exception as e:
            raise FaceRecognitionException(f"Face detection failed: {str(e)}")
    
    async def verify_face(self, emp_id: str, image_data: str) -> Dict[str, Any]:
        """Verify if face in image matches registered employee."""
        try:
            employee = await self.employee_service.get_employee_by_id(emp_id)
            if not employee or not employee.has_face_encoding():
                return {
                    "verified": False,
                    "message": "Employee not found or no face registered",
                    "confidence": 0.0
                }
            
            image = self._decode_base64_image(image_data)
            
            # Generate embedding from new image
            try:
                # Convert to RGB for DeepFace
                if len(image.shape) == 3:
                    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                else:
                    rgb_image = image
                
                embedding_objs = DeepFace.represent(
                    rgb_image,
                    enforce_detection=True,
                    detector_backend='opencv',
                    model_name='VGG-Face'
                )
                
                if not embedding_objs:
                    return {
                        "verified": False,
                        "message": "No face detected in image",
                        "confidence": 0.0
                    }
                
                new_embedding = np.array(embedding_objs[0]['embedding'])
                
            except Exception as e:
                return {
                    "verified": False,
                    "message": f"Face detection failed: {str(e)}",
                    "confidence": 0.0
                }
            
            # Compare with registered embedding
            try:
                result = DeepFace.verify(
                    employee.face_encoding,
                    new_embedding,
                    model_name='VGG-Face',
                    detector_backend='opencv'
                )
                
                distance = result['distance']
                confidence = 1 - distance
                verified = distance <= settings.deepface_tolerance
                
                return {
                    "verified": verified,
                    "confidence": float(confidence),
                    "distance": float(distance),
                    "message": "Face verified successfully" if verified else "Face verification failed"
                }
                
            except Exception as e:
                return {
                    "verified": False,
                    "message": f"Face verification failed: {str(e)}",
                    "confidence": 0.0
                }
            
        except Exception as e:
            raise FaceRecognitionException(f"Face verification failed: {str(e)}")
    
    def _find_best_match(self, unknown_encoding: np.ndarray) -> Tuple[Optional[str], float]:
        """Find best match for unknown encoding."""
        best_match_id = None
        best_confidence = 0.0
        best_distance = float('inf')
        
        for i, known_encoding in enumerate(self.known_face_encodings):
            try:
                result = DeepFace.verify(
                    known_encoding,
                    unknown_encoding,
                    model_name='VGG-Face',
                    detector_backend='opencv'
                )
                
                distance = result['distance']
                confidence = 1 - distance
                
                if distance <= settings.deepface_tolerance and confidence > best_confidence:
                    best_confidence = confidence
                    best_distance = distance
                    best_match_id = self.known_employee_ids[i]
                    
            except Exception:
                continue
        
        return best_match_id, best_confidence
    
    def _average_encodings(self, encodings: List[np.ndarray]) -> np.ndarray:
        """Average multiple encodings for better accuracy."""
        return np.mean(encodings, axis=0)
    
    def _decode_base64_image(self, image_data: str) -> np.ndarray:
        """Decode base64 image to numpy array."""
        try:
            # Remove data URL prefix if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode base64
            image_bytes = base64.b64decode(image_data)
            
            # Convert to PIL Image
            pil_image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Convert to numpy array
            image_array = np.array(pil_image)
            
            # Convert BGR to RGB for DeepFace library
            if len(image_array.shape) == 3:
                image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
            
            return image_array
            
        except Exception as e:
            raise ValidationException(f"Invalid image data: {str(e)}")
    
    def _assess_image_quality(self, image: np.ndarray) -> float:
        """Assess image quality based on various factors."""
        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Calculate sharpness using Laplacian variance
            sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Normalize sharpness score (0-1 range)
            max_sharpness = 1000.0  # Adjust based on testing
            sharpness_score = min(sharpness / max_sharpness, 1.0)
            
            # Calculate brightness
            brightness = np.mean(gray) / 255.0
            
            # Penalize too dark or too bright images
            if brightness < 0.2 or brightness > 0.8:
                brightness_score = 0.5
            else:
                brightness_score = 1.0
            
            # Calculate contrast
            contrast = np.std(gray) / 255.0
            contrast_score = min(contrast * 2, 1.0)  # Normalize to 0-1
            
            # Combine scores
            quality_score = (sharpness_score * 0.5 + brightness_score * 0.3 + contrast_score * 0.2)
            
            return quality_score
            
        except Exception:
            return 0.0  # Return lowest quality if assessment fails
    
    async def _load_known_face_encodings(self) -> None:
        """Load known face encodings from database."""
        try:
            # Get all employees with face encodings
            employees = await self.employee_service.get_employees_with_face_encoding()
            
            self.known_face_encodings = []
            self.known_employee_ids = []
            
            for employee in employees:
                if employee.has_face_encoding():
                    self.known_face_encodings.append(np.array(employee.face_encoding))
                    self.known_employee_ids.append(employee.emp_id)
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to load known face encodings: {str(e)}")
    
    def get_face_detection_info(self, image_data: str) -> Dict[str, Any]:
        """Get face detection information from image using DeepFace."""
        try:
            # Decode image
            image = self._decode_base64_image(image_data)
            
            # Convert to RGB for DeepFace
            if len(image.shape) == 3:
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                rgb_image = image
            
            # Detect faces using DeepFace
            try:
                face_objs = DeepFace.analyze(
                    rgb_image,
                    actions=['age', 'gender', 'emotion'],
                    enforce_detection=False,
                    detector_backend='opencv'
                )
                
                # Prepare detection info
                detections = []
                for i, face_obj in enumerate(face_objs):
                    if 'region' in face_obj:
                        region = face_obj['region']
                        x, y, w, h = region['x'], region['y'], region['w'], region['h']
                        
                        detections.append({
                            "face_id": i,
                            "location": {
                                "top": y,
                                "right": x + w,
                                "bottom": y + h,
                                "left": x
                            },
                            "face_area": w * h,
                            "confidence": face_obj.get('confidence', 0.0),
                            "age": face_obj.get('age', 0),
                            "gender": face_obj.get('dominant_gender', 'unknown'),
                            "emotion": face_obj.get('dominant_emotion', 'unknown')
                        })
                
            except Exception:
                detections = []
            
            # Assess overall image quality
            quality_score = self._assess_image_quality(image)
            
            return {
                "faces_detected": len(detections),
                "quality_score": round(quality_score, 3),
                "image_shape": image.shape,
                "detections": detections
            }
            
        except Exception as e:
            raise FaceRecognitionException(f"Face detection failed: {str(e)}")
    
    def validate_face_image(self, image_data: str) -> Dict[str, Any]:
        """Validate face image for registration."""
        try:
            # Get face detection info
            detection_info = self.get_face_detection_info(image_data)
            
            # Validation rules
            validation_errors = []
            
            # Check if exactly one face is detected
            if detection_info["faces_detected"] == 0:
                validation_errors.append("No face detected in image")
            elif detection_info["faces_detected"] > 1:
                validation_errors.append("Multiple faces detected. Only one face should be present")
            
            # Check image quality
            if detection_info["quality_score"] < settings.image_quality_threshold:
                validation_errors.append(
                    f"Image quality too low: {detection_info['quality_score']:.3f} "
                    f"(minimum: {settings.image_quality_threshold})"
                )
            
            # Check face size
            if detection_info["detections"]:
                face_area = detection_info["detections"][0]["face_area"]
                min_face_area = 10000  # Minimum face area in pixels
                if face_area < min_face_area:
                    validation_errors.append("Face too small in image")
            
            return {
                "valid": len(validation_errors) == 0,
                "errors": validation_errors,
                "detection_info": detection_info
            }
            
        except Exception as e:
            return {
                "valid": False,
                "errors": [f"Validation failed: {str(e)}"],
                "detection_info": None
            }
