"""
Face encoding utilities and helpers.
"""

import numpy as np
from deepface import DeepFace
from typing import List, Tuple, Optional
import cv2

from app.core.config import settings
from app.core.exceptions import FaceRecognitionException


class FaceEncodingUtils:
    """Utilities for face encoding operations."""
    
    @staticmethod
    def generate_encoding(image: np.ndarray, face_location: Tuple[int, int, int, int] = None) -> Optional[np.ndarray]:
        """Generate face encoding from image using DeepFace."""
        try:
            # Convert image to RGB for DeepFace
            if len(image.shape) == 3:
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                rgb_image = image
            
            # Use DeepFace to get face embedding
            embedding_objs = DeepFace.represent(
                rgb_image,
                enforce_detection=False,
                detector_backend='opencv',
                model_name='VGG-Face'
            )
            
            if embedding_objs:
                return np.array(embedding_objs[0]['embedding'])
            return None
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to generate face encoding: {str(e)}")
    
    @staticmethod
    def compare_encodings(known_encoding: np.ndarray, unknown_encoding: np.ndarray, tolerance: float = None) -> Tuple[bool, float]:
        """Compare two face encodings using DeepFace."""
        try:
            if tolerance is None:
                tolerance = settings.deepface_tolerance
            
            # Calculate cosine similarity using DeepFace
            distance = DeepFace.verify(
                known_encoding,
                unknown_encoding,
                model_name='VGG-Face',
                detector_backend='opencv'
            )['distance']
            
            # Determine if faces match (lower distance means more similar)
            match = distance <= tolerance
            confidence = 1 - distance
            
            return match, float(confidence)
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to compare face encodings: {str(e)}")
    
    @staticmethod
    def find_best_match(unknown_encoding: np.ndarray, known_encodings: List[np.ndarray], 
                       known_ids: List[str], tolerance: float = None) -> Tuple[Optional[str], float]:
        """Find best match for unknown encoding among known encodings."""
        try:
            if not known_encodings:
                return None, 0.0
            
            if tolerance is None:
                tolerance = settings.deepface_tolerance
            
            best_match_id = None
            best_confidence = 0.0
            best_distance = float('inf')
            
            # Compare with all known encodings
            for i, known_encoding in enumerate(known_encodings):
                try:
                    result = DeepFace.verify(
                        known_encoding,
                        unknown_encoding,
                        model_name='VGG-Face',
                        detector_backend='opencv'
                    )
                    
                    distance = result['distance']
                    confidence = 1 - distance
                    
                    if distance <= tolerance and confidence > best_confidence:
                        best_confidence = confidence
                        best_distance = distance
                        best_match_id = known_ids[i]
                        
                except Exception:
                    continue
            
            return best_match_id, best_confidence
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to find best match: {str(e)}")
    
    @staticmethod
    def average_encodings(encodings: List[np.ndarray]) -> np.ndarray:
        """Average multiple face encodings to create a more robust encoding."""
        try:
            if not encodings:
                raise ValueError("No encodings provided")
            
            # Convert to numpy array and calculate mean
            encoding_array = np.array(encodings)
            averaged_encoding = np.mean(encoding_array, axis=0)
            
            # Normalize the encoding
            norm = np.linalg.norm(averaged_encoding)
            if norm > 0:
                averaged_encoding = averaged_encoding / norm
            
            return averaged_encoding
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to average encodings: {str(e)}")
    
    @staticmethod
    def validate_encoding(encoding: np.ndarray) -> bool:
        """Validate face encoding format and dimensions."""
        try:
            # Check if encoding is a numpy array
            if not isinstance(encoding, np.ndarray):
                return False
            
            # Check dimensions (DeepFace VGG-Face produces 128-dimensional embeddings)
            if encoding.shape != (128,):
                return False
            
            # Check for NaN or infinite values
            if np.any(np.isnan(encoding)) or np.any(np.isinf(encoding)):
                return False
            
            # Check if encoding is normalized (optional)
            norm = np.linalg.norm(encoding)
            if norm == 0:
                return False
            
            return True
            
        except Exception:
            return False
    
    @staticmethod
    def encoding_to_list(encoding: np.ndarray) -> List[float]:
        """Convert numpy encoding to list for storage."""
        try:
            if not FaceEncodingUtils.validate_encoding(encoding):
                raise ValueError("Invalid encoding")
            
            return encoding.tolist()
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to convert encoding to list: {str(e)}")
    
    @staticmethod
    def list_to_encoding(encoding_list: List[float]) -> np.ndarray:
        """Convert list to numpy encoding."""
        try:
            encoding = np.array(encoding_list, dtype=np.float64)
            
            if not FaceEncodingUtils.validate_encoding(encoding):
                raise ValueError("Invalid encoding list")
            
            return encoding
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to convert list to encoding: {str(e)}")
    
    @staticmethod
    def calculate_encoding_similarity(encoding1: np.ndarray, encoding2: np.ndarray) -> float:
        """Calculate similarity score between two encodings."""
        try:
            if not (FaceEncodingUtils.validate_encoding(encoding1) and 
                   FaceEncodingUtils.validate_encoding(encoding2)):
                raise ValueError("Invalid encodings")
            
            # Calculate cosine similarity
            dot_product = np.dot(encoding1, encoding2)
            norm1 = np.linalg.norm(encoding1)
            norm2 = np.linalg.norm(encoding2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = dot_product / (norm1 * norm2)
            return float(similarity)
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to calculate encoding similarity: {str(e)}")
    
    @staticmethod
    def enhance_encoding_quality(encodings: List[np.ndarray], quality_threshold: float = 0.7) -> np.ndarray:
        """Enhance encoding quality by filtering and averaging high-quality encodings."""
        try:
            if not encodings:
                raise ValueError("No encodings provided")
            
            # Filter encodings based on quality (simplified - would need actual quality assessment)
            quality_scores = []
            for encoding in encodings:
                # Simple quality check based on encoding characteristics
                norm = np.linalg.norm(encoding)
                variance = np.var(encoding)
                quality_score = min(norm * variance, 1.0)  # Simplified quality metric
                quality_scores.append(quality_score)
            
            # Filter high-quality encodings
            high_quality_encodings = [
                enc for enc, score in zip(encodings, quality_scores) 
                if score >= quality_threshold
            ]
            
            if not high_quality_encodings:
                # If no high-quality encodings, use all
                high_quality_encodings = encodings
            
            # Average the filtered encodings
            return FaceEncodingUtils.average_encodings(high_quality_encodings)
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to enhance encoding quality: {str(e)}")
