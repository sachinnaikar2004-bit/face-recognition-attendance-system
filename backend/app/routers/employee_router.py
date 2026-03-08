"""
Employee management router.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.schemas.employee_schema import (
    EmployeeCreate, EmployeeUpdate, EmployeeResponse, 
    EmployeeListResponse, EmployeeSearchFilter
)
from app.schemas.response_schema import SuccessResponse
from app.services.employee_service import EmployeeService
from app.services.auth_service import AuthService
from app.dependencies.auth_dependency import get_current_user
from app.core.exceptions import (
    NotFoundException, DuplicateResourceException, 
    ValidationException, DatabaseException
)

router = APIRouter(prefix="/employees", tags=["employees"])
employee_service = EmployeeService()
auth_service = AuthService()


@router.get("/", response_model=EmployeeListResponse)
async def get_employees(
    filters: EmployeeSearchFilter = EmployeeSearchFilter(),
    current_user: dict = Depends(get_current_user)
):
    """Get all employees with optional filtering and pagination."""
    try:
        employees, pagination = await employee_service.get_employees(filters)
        
        employee_responses = [
            EmployeeResponse(
                id=str(emp.id),
                emp_id=emp.emp_id,
                name=emp.name,
                email=emp.email,
                role=emp.role,
                department=emp.department,
                created_at=emp.created_at,
                updated_at=emp.updated_at,
                last_login=emp.last_login,
                is_active=emp.is_active,
                has_face_encoding=emp.has_face_encoding()
            )
            for emp in employees
        ]
        
        return EmployeeListResponse(
            employees=employee_responses,
            pagination=pagination
        )
        
    except (NotFoundException, DuplicateResourceException, ValidationException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", response_model=EmployeeResponse)
async def create_employee(
    employee_data: EmployeeCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new employee (admin only)."""
    try:
        # Require admin access
        await auth_service.authorize_admin(current_user)
        
        # Create employee
        employee = await employee_service.create_employee(employee_data)
        
        return EmployeeResponse(
            id=str(employee.id),
            emp_id=employee.emp_id,
            name=employee.name,
            email=employee.email,
            role=employee.role,
            department=employee.department,
            created_at=employee.created_at,
            updated_at=employee.updated_at,
            last_login=employee.last_login,
            is_active=employee.is_active,
            has_face_encoding=employee.has_face_encoding()
        )
        
    except (NotFoundException, DuplicateResourceException, ValidationException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{emp_id}", response_model=EmployeeResponse)
async def get_employee(
    emp_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get employee by ID."""
    try:
        employee = await employee_service.get_employee_by_id(emp_id)
        
        return EmployeeResponse(
            id=str(employee.id),
            emp_id=employee.emp_id,
            name=employee.name,
            email=employee.email,
            role=employee.role,
            department=employee.department,
            created_at=employee.created_at,
            updated_at=employee.updated_at,
            last_login=employee.last_login,
            is_active=employee.is_active,
            has_face_encoding=employee.has_face_encoding()
        )
        
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{emp_id}", response_model=EmployeeResponse)
async def update_employee(
    emp_id: str,
    update_data: EmployeeUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update employee information (admin only)."""
    try:
        # Require admin access
        await auth_service.authorize_admin(current_user)
        
        # Update employee
        employee = await employee_service.update_employee(emp_id, update_data)
        
        return EmployeeResponse(
            id=str(employee.id),
            emp_id=employee.emp_id,
            name=employee.name,
            email=employee.email,
            role=employee.role,
            department=employee.department,
            created_at=employee.created_at,
            updated_at=employee.updated_at,
            last_login=employee.last_login,
            is_active=employee.is_active,
            has_face_encoding=employee.has_face_encoding()
        )
        
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (DuplicateResourceException, ValidationException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{emp_id}")
async def delete_employee(
    emp_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete employee (admin only)."""
    try:
        # Require admin access and prevent self-deletion
        await auth_service.deactivate_employee(emp_id, current_user)
        
        return SuccessResponse(
            message="Employee deleted successfully"
        )
        
    except (NotFoundException, ValidationException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{emp_id}/recapture-face")
async def recapture_face(
    emp_id: str,
    face_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Recapture employee face image."""
    try:
        # Validate access
        await auth_service.validate_face_registration_access(emp_id, current_user)
        
        # Validate face image
        face_image = face_data.get("face_image")
        if not face_image:
            raise ValidationException("Face image is required")
        
        # Register face
        face_service = employee_service.face_service if hasattr(employee_service, 'face_service') else None
        if not face_service:
            from app.services.face_service import FaceService
            face_service = FaceService()
        
        result = await face_service.register_face(emp_id, [face_image])
        
        return SuccessResponse(
            data=result,
            message="Face image updated successfully"
        )
        
    except (NotFoundException, ValidationException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/stats/summary")
async def get_employee_stats(
    current_user: dict = Depends(get_current_user)
):
    """Get employee statistics (admin only)."""
    try:
        # Require admin access
        await auth_service.authorize_admin(current_user)
        
        stats = await employee_service.get_employee_stats()
        
        return SuccessResponse(
            data=stats,
            message="Employee statistics retrieved successfully"
        )
        
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
