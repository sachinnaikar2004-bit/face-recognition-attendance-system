"""
Face recognition router.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from app.schemas.auth_schema import (
    LoginRequest, FaceLoginResponse, FaceLogoutResponse,
    FaceRegisterRequest, FaceRegisterResponse, FaceRecognitionResponse
)
from app.schemas.response_schema import SuccessResponse
from app.services.face_service import FaceService
from app.services.auth_service import AuthService
from app.services.attendance_service import AttendanceService
from app.dependencies.auth_dependency import get_current_user
from app.core.exceptions import (
    FaceRecognitionException, ValidationException, 
    AuthenticationException, DatabaseException
)

router = APIRouter(prefix="/face", tags=["face"])
face_service = FaceService()
auth_service = AuthService()
attendance_service = AttendanceService()


@router.post("/login", response_model=FaceLoginResponse)
async def face_login(login_request: LoginRequest):
    """Login using face recognition."""
    try:
        # Authenticate with face
        login_data = await auth_service.login_with_face(login_request.face_image)
        
        return FaceLoginResponse(
            success=True,
            data=login_data,
            message="Login successful"
        )
        
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except FaceRecognitionException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/logout", response_model=FaceLogoutResponse)
async def face_logout(
    logout_request: LoginRequest,
    current_user: dict = Depends(get_current_user)
):
    """Logout using face verification."""
    try:
        # Verify face and logout
        logout_data = await auth_service.logout_with_face(logout_request.face_image, current_user)
        
        return FaceLogoutResponse(
            success=True,
            data=logout_data,
            message="Logout successful"
        )
        
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except FaceRecognitionException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/register", response_model=FaceRegisterResponse)
async def register_face(
    register_request: FaceRegisterRequest,
    current_user: dict = Depends(get_current_user)
):
    """Register face for employee."""
    try:
        # Validate access
        await auth_service.validate_face_registration_access(
            register_request.emp_id, 
            current_user
        )
        
        # Register face
        result = await face_service.register_face(
            register_request.emp_id, 
            register_request.face_images
        )
        
        return FaceRegisterResponse(
            success=True,
            data=result,
            message="Face registered successfully"
        )
        
    except (ValidationException, AuthenticationException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except FaceRecognitionException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/verify", response_model=FaceRecognitionResponse)
async def verify_face(verify_request: LoginRequest):
    """Verify face without marking attendance."""
    try:
        # Verify face
        result = await face_service.verify_face(verify_request.face_image)
        
        if result["verified"]:
            return FaceRecognitionResponse(
                verified=True,
                emp_id=result["emp_id"],
                name=result["name"],
                confidence=result["confidence"],
                message="Face verified successfully"
            )
        else:
            return FaceRecognitionResponse(
                verified=False,
                message=result.get("message", "Face verification failed")
            )
        
    except FaceRecognitionException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/detect")
async def detect_faces(detect_request: LoginRequest):
    """Detect faces in image and return detection info."""
    try:
        # Get face detection info
        detection_info = face_service.get_face_detection_info(detect_request.face_image)
        
        return SuccessResponse(
            data=detection_info,
            message="Face detection completed"
        )
        
    except FaceRecognitionException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/validate")
async def validate_face_image(validate_request: LoginRequest):
    """Validate face image for registration."""
    try:
        # Validate face image
        validation_result = face_service.validate_face_image(validate_request.face_image)
        
        return SuccessResponse(
            data=validation_result,
            message="Face validation completed"
        )
        
    except FaceRecognitionException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/quality/{emp_id}")
async def get_face_quality_info(
    emp_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get face quality information for employee."""
    try:
        # Validate access
        await auth_service.validate_face_registration_access(emp_id, current_user)
        
        # Get employee info
        employee_service = auth_service.employee_service
        employee = await employee_service.get_employee_by_id(emp_id)
        
        # Check if employee has face encoding
        has_encoding = employee.has_face_encoding()
        
        quality_info = {
            "emp_id": emp_id,
            "has_face_encoding": has_encoding,
            "encoding_length": len(employee.face_encoding) if has_encoding else 0,
            "can_register": not has_encoding,
            "last_updated": employee.updated_at
        }
        
        return SuccessResponse(
            data=quality_info,
            message="Face quality information retrieved"
        )
        
    except (ValidationException, AuthenticationException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/remove/{emp_id}")
async def remove_face_encoding(
    emp_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Remove face encoding for employee."""
    try:
        # Validate access
        await auth_service.validate_face_registration_access(emp_id, current_user)
        
        # Remove face encoding
        employee_service = auth_service.employee_service
        await employee_service.update_face_encoding(emp_id, [])
        
        return SuccessResponse(
            message="Face encoding removed successfully"
        )
        
    except (ValidationException, AuthenticationException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/stats/summary")
async def get_deepface_stats(
    current_user: dict = Depends(get_current_user)
):
    """Get face recognition statistics (admin only)."""
    try:
        # Require admin access
        await auth_service.authorize_admin(current_user)
        
        # Get employee stats
        employee_service = auth_service.employee_service
        employee_stats = await employee_service.get_employee_stats()
        
        # Get employees with face encoding
        employees_with_encoding = await employee_service.get_employees_with_face_encoding()
        
        stats = {
            "total_employees": employee_stats.get("total_employees", 0),
            "employees_with_face_encoding": len(employees_with_encoding),
            "employees_without_face_encoding": employee_stats.get("total_employees", 0) - len(employees_with_encoding),
            "face_registration_rate": round(
                (len(employees_with_encoding) / employee_stats.get("total_employees", 1)) * 100, 2
            )
        }
        
        return SuccessResponse(
            data=stats,
            message="Face recognition statistics retrieved"
        )
        
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
