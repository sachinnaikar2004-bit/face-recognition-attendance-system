"""
Camera capture utilities for face recognition.
"""

import cv2
import numpy as np
import base64
import io
from PIL import Image
from typing import Optional, Tuple, List
import time

from app.core.exceptions import FaceRecognitionException


class CameraUtils:
    """Utilities for camera operations and frame capture."""
    
    @staticmethod
    def initialize_camera(camera_id: int = 0, width: int = 640, height: int = 480) -> cv2.VideoCapture:
        """Initialize camera with specified settings."""
        try:
            cap = cv2.VideoCapture(camera_id)
            
            if not cap.isOpened():
                raise FaceRecognitionException(f"Failed to open camera {camera_id}")
            
            # Set camera properties
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            cap.set(cv2.CAP_PROP_FPS, 30)
            
            return cap
            
        except Exception as e:
            raise FaceRecognitionException(f"Camera initialization failed: {str(e)}")
    
    @staticmethod
    def capture_frame(cap: cv2.VideoCapture) -> Optional[np.ndarray]:
        """Capture single frame from camera."""
        try:
            ret, frame = cap.read()
            
            if not ret:
                raise FaceRecognitionException("Failed to capture frame from camera")
            
            return frame
            
        except Exception as e:
            raise FaceRecognitionException(f"Frame capture failed: {str(e)}")
    
    @staticmethod
    def release_camera(cap: cv2.VideoCapture) -> None:
        """Release camera resources."""
        try:
            if cap.isOpened():
                cap.release()
        except Exception:
            pass  # Ignore errors during cleanup
    
    @staticmethod
    def frame_to_base64(frame: np.ndarray, quality: int = 85) -> str:
        """Convert frame to base64 string."""
        try:
            # Convert BGR to RGB
            if len(frame.shape) == 3:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                frame_rgb = frame
            
            # Convert to PIL Image
            pil_image = Image.fromarray(frame_rgb)
            
            # Save to bytes
            buffer = io.BytesIO()
            pil_image.save(buffer, format='JPEG', quality=quality)
            buffer.seek(0)
            
            # Encode to base64
            image_bytes = buffer.getvalue()
            base64_string = base64.b64encode(image_bytes).decode('utf-8')
            
            return base64_string
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to convert frame to base64: {str(e)}")
    
    @staticmethod
    def base64_to_frame(base64_string: str) -> np.ndarray:
        """Convert base64 string to frame."""
        try:
            # Remove data URL prefix if present
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            # Decode base64
            image_bytes = base64.b64decode(base64_string)
            
            # Convert to PIL Image
            pil_image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to numpy array (RGB)
            frame = np.array(pil_image)
            
            # Convert RGB to BGR for OpenCV
            if len(frame.shape) == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            return frame
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to convert base64 to frame: {str(e)}")
    
    @staticmethod
    def resize_frame(frame: np.ndarray, width: int, height: int) -> np.ndarray:
        """Resize frame to specified dimensions."""
        try:
            return cv2.resize(frame, (width, height))
        except Exception as e:
            raise FaceRecognitionException(f"Failed to resize frame: {str(e)}")
    
    @staticmethod
    def crop_face_region(frame: np.ndarray, face_location: Tuple[int, int, int, int], 
                        padding: int = 20) -> np.ndarray:
        """Crop face region from frame."""
        try:
            top, right, bottom, left = face_location
            
            # Add padding
            top = max(0, top - padding)
            right = min(frame.shape[1], right + padding)
            bottom = min(frame.shape[0], bottom + padding)
            left = max(0, left - padding)
            
            # Crop face region
            face_region = frame[top:bottom, left:right]
            
            return face_region
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to crop face region: {str(e)}")
    
    @staticmethod
    def enhance_frame_quality(frame: np.ndarray) -> np.ndarray:
        """Enhance frame quality for better face recognition."""
        try:
            # Convert to grayscale for processing
            if len(frame.shape) == 3:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                gray = frame
            
            # Apply histogram equalization
            enhanced = cv2.equalizeHist(gray)
            
            # Apply Gaussian blur to reduce noise
            enhanced = cv2.GaussianBlur(enhanced, (3, 3), 0)
            
            # Convert back to original format
            if len(frame.shape) == 3:
                enhanced = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
            
            return enhanced
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to enhance frame quality: {str(e)}")
    
    @staticmethod
    def detect_faces_in_frame(frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect faces in frame using OpenCV."""
        try:
            # Convert to grayscale
            if len(frame.shape) == 3:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                gray = frame
            
            # Load face cascade classifier
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # Detect faces
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            # Convert to DeepFace format (top, right, bottom, left)
            face_locations = []
            for (x, y, w, h) in faces:
                face_locations.append((y, x + w, y + h, x))
            
            return face_locations
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to detect faces: {str(e)}")
    
    @staticmethod
    def validate_frame_quality(frame: np.ndarray) -> dict:
        """Validate frame quality for face recognition."""
        try:
            quality_info = {
                "valid": True,
                "issues": [],
                "metrics": {}
            }
            
            # Check frame dimensions
            if len(frame.shape) < 2:
                quality_info["valid"] = False
                quality_info["issues"].append("Invalid frame dimensions")
                return quality_info
            
            height, width = frame.shape[:2]
            quality_info["metrics"]["resolution"] = f"{width}x{height}"
            
            # Check minimum resolution
            if width < 320 or height < 240:
                quality_info["valid"] = False
                quality_info["issues"].append("Resolution too low (minimum 320x240)")
            
            # Check brightness
            if len(frame.shape) == 3:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                gray = frame
            
            brightness = np.mean(gray)
            quality_info["metrics"]["brightness"] = round(brightness, 2)
            
            if brightness < 50:
                quality_info["issues"].append("Image too dark")
            elif brightness > 200:
                quality_info["issues"].append("Image too bright")
            
            # Check contrast
            contrast = np.std(gray)
            quality_info["metrics"]["contrast"] = round(contrast, 2)
            
            if contrast < 30:
                quality_info["issues"].append("Low contrast")
            
            # Check blur
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            quality_info["metrics"]["sharpness"] = round(laplacian_var, 2)
            
            if laplacian_var < 100:
                quality_info["issues"].append("Image too blurry")
            
            return quality_info
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to validate frame quality: {str(e)}")
    
    @staticmethod
    def create_camera_info() -> dict:
        """Get camera information."""
        try:
            camera_info = {
                "available_cameras": [],
                "default_camera": 0
            }
            
            # Test available cameras
            for i in range(5):  # Check first 5 camera indices
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    # Get camera properties
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = int(cap.get(cv2.CAP_PROP_FPS))
                    
                    camera_info["available_cameras"].append({
                        "id": i,
                        "resolution": f"{width}x{height}",
                        "fps": fps
                    })
                    cap.release()
                else:
                    break
            
            return camera_info
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to get camera info: {str(e)}")
