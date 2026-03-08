"""
Image processing utilities for face recognition.
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from typing import Tuple, Optional
import base64
import io

from app.core.exceptions import FaceRecognitionException


class ImageProcessingUtils:
    """Utilities for image processing operations."""
    
    @staticmethod
    def resize_image(image: np.ndarray, target_size: Tuple[int, int], 
                    maintain_aspect_ratio: bool = True) -> np.ndarray:
        """Resize image to target size."""
        try:
            height, width = image.shape[:2]
            target_width, target_height = target_size
            
            if maintain_aspect_ratio:
                # Calculate aspect ratio
                aspect_ratio = width / height
                
                # Calculate new dimensions
                if target_width / target_height > aspect_ratio:
                    new_height = target_height
                    new_width = int(target_height * aspect_ratio)
                else:
                    new_width = target_width
                    new_height = int(target_width / aspect_ratio)
                
                # Resize image
                resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
                
                # Create canvas with target size and center the image
                canvas = np.zeros((target_height, target_width, 3), dtype=np.uint8)
                y_offset = (target_height - new_height) // 2
                x_offset = (target_width - new_width) // 2
                canvas[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized
                
                return canvas
            else:
                return cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
                
        except Exception as e:
            raise FaceRecognitionException(f"Failed to resize image: {str(e)}")
    
    @staticmethod
    def normalize_image(image: np.ndarray) -> np.ndarray:
        """Normalize image pixel values."""
        try:
            # Convert to float and normalize to 0-1 range
            normalized = image.astype(np.float32) / 255.0
            
            # Convert back to uint8
            normalized = (normalized * 255).astype(np.uint8)
            
            return normalized
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to normalize image: {str(e)}")
    
    @staticmethod
    def enhance_brightness(image: np.ndarray, factor: float = 1.2) -> np.ndarray:
        """Enhance image brightness."""
        try:
            # Convert to PIL Image
            if len(image.shape) == 3:
                pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            else:
                pil_image = Image.fromarray(image)
            
            # Enhance brightness
            enhancer = ImageEnhance.Brightness(pil_image)
            enhanced = enhancer.enhance(factor)
            
            # Convert back to numpy array
            enhanced_array = np.array(enhanced)
            
            if len(image.shape) == 3:
                return cv2.cvtColor(enhanced_array, cv2.COLOR_RGB2BGR)
            else:
                return enhanced_array
                
        except Exception as e:
            raise FaceRecognitionException(f"Failed to enhance brightness: {str(e)}")
    
    @staticmethod
    def enhance_contrast(image: np.ndarray, factor: float = 1.2) -> np.ndarray:
        """Enhance image contrast."""
        try:
            # Convert to PIL Image
            if len(image.shape) == 3:
                pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            else:
                pil_image = Image.fromarray(image)
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(pil_image)
            enhanced = enhancer.enhance(factor)
            
            # Convert back to numpy array
            enhanced_array = np.array(enhanced)
            
            if len(image.shape) == 3:
                return cv2.cvtColor(enhanced_array, cv2.COLOR_RGB2BGR)
            else:
                return enhanced_array
                
        except Exception as e:
            raise FaceRecognitionException(f"Failed to enhance contrast: {str(e)}")
    
    @staticmethod
    def enhance_sharpness(image: np.ndarray, factor: float = 1.2) -> np.ndarray:
        """Enhance image sharpness."""
        try:
            # Convert to PIL Image
            if len(image.shape) == 3:
                pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            else:
                pil_image = Image.fromarray(image)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(pil_image)
            enhanced = enhancer.enhance(factor)
            
            # Convert back to numpy array
            enhanced_array = np.array(enhanced)
            
            if len(image.shape) == 3:
                return cv2.cvtColor(enhanced_array, cv2.COLOR_RGB2BGR)
            else:
                return enhanced_array
                
        except Exception as e:
            raise FaceRecognitionException(f"Failed to enhance sharpness: {str(e)}")
    
    @staticmethod
    def remove_noise(image: np.ndarray, method: str = "gaussian") -> np.ndarray:
        """Remove noise from image."""
        try:
            if method == "gaussian":
                return cv2.GaussianBlur(image, (3, 3), 0)
            elif method == "median":
                return cv2.medianBlur(image, 3)
            elif method == "bilateral":
                return cv2.bilateralFilter(image, 9, 75, 75)
            else:
                return cv2.GaussianBlur(image, (3, 3), 0)
                
        except Exception as e:
            raise FaceRecognitionException(f"Failed to remove noise: {str(e)}")
    
    @staticmethod
    def histogram_equalization(image: np.ndarray) -> np.ndarray:
        """Apply histogram equalization to improve contrast."""
        try:
            if len(image.shape) == 3:
                # Convert to YUV color space
                yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
                
                # Apply histogram equalization to Y channel
                yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
                
                # Convert back to BGR
                return cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
            else:
                # Apply to grayscale image
                return cv2.equalizeHist(image)
                
        except Exception as e:
            raise FaceRecognitionException(f"Failed to apply histogram equalization: {str(e)}")
    
    @staticmethod
    def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
        """Rotate image by specified angle."""
        try:
            height, width = image.shape[:2]
            center = (width // 2, height // 2)
            
            # Get rotation matrix
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            
            # Apply rotation
            rotated = cv2.warpAffine(image, rotation_matrix, (width, height))
            
            return rotated
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to rotate image: {str(e)}")
    
    @staticmethod
    def crop_center(image: np.ndarray, crop_size: Tuple[int, int]) -> np.ndarray:
        """Crop center region of image."""
        try:
            height, width = image.shape[:2]
            crop_width, crop_height = crop_size
            
            # Calculate crop coordinates
            start_x = max(0, (width - crop_width) // 2)
            start_y = max(0, (height - crop_height) // 2)
            end_x = min(width, start_x + crop_width)
            end_y = min(height, start_y + crop_height)
            
            # Crop image
            cropped = image[start_y:end_y, start_x:end_x]
            
            return cropped
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to crop image: {str(e)}")
    
    @staticmethod
    def auto_orient_image(image: np.ndarray) -> np.ndarray:
        """Automatically orient image based on EXIF data."""
        try:
            # Convert to PIL Image to read EXIF
            if len(image.shape) == 3:
                pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            else:
                pil_image = Image.fromarray(image)
            
            # Get EXIF data
            exif = pil_image._getexif()
            
            if exif is not None:
                # Get orientation tag
                orientation = exif.get(0x0112, 1)
                
                # Apply orientation correction
                if orientation == 3:
                    pil_image = pil_image.rotate(180, expand=True)
                elif orientation == 6:
                    pil_image = pil_image.rotate(270, expand=True)
                elif orientation == 8:
                    pil_image = pil_image.rotate(90, expand=True)
            
            # Convert back to numpy array
            oriented_array = np.array(pil_image)
            
            if len(image.shape) == 3:
                return cv2.cvtColor(oriented_array, cv2.COLOR_RGB2BGR)
            else:
                return oriented_array
                
        except Exception:
            # If orientation fails, return original image
            return image
    
    @staticmethod
    def enhance_for_deepface(image: np.ndarray) -> np.ndarray:
        """Apply optimal enhancements for face recognition."""
        try:
            # Auto orient image
            enhanced = ImageProcessingUtils.auto_orient_image(image)
            
            # Remove noise
            enhanced = ImageProcessingUtils.remove_noise(enhanced, "bilateral")
            
            # Apply histogram equalization
            enhanced = ImageProcessingUtils.histogram_equalization(enhanced)
            
            # Enhance contrast slightly
            enhanced = ImageProcessingUtils.enhance_contrast(enhanced, 1.1)
            
            # Enhance sharpness slightly
            enhanced = ImageProcessingUtils.enhance_sharpness(enhanced, 1.1)
            
            return enhanced
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to enhance image for face recognition: {str(e)}")
    
    @staticmethod
    def validate_image_format(image_data: str) -> bool:
        """Validate if image data is in supported format."""
        try:
            # Remove data URL prefix if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode base64
            image_bytes = base64.b64decode(image_data)
            
            # Try to open with PIL
            pil_image = Image.open(io.BytesIO(image_bytes))
            
            # Check if format is supported
            supported_formats = ['JPEG', 'PNG', 'BMP', 'TIFF']
            return pil_image.format in supported_formats
            
        except Exception:
            return False
    
    @staticmethod
    def get_image_info(image_data: str) -> dict:
        """Get image information."""
        try:
            # Remove data URL prefix if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode base64
            image_bytes = base64.b64decode(image_data)
            
            # Get image info
            pil_image = Image.open(io.BytesIO(image_bytes))
            
            info = {
                "format": pil_image.format,
                "mode": pil_image.mode,
                "size": pil_image.size,
                "width": pil_image.width,
                "height": pil_image.height,
                "file_size": len(image_bytes)
            }
            
            return info
            
        except Exception as e:
            raise FaceRecognitionException(f"Failed to get image info: {str(e)}")
