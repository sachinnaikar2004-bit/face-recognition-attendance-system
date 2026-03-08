"""
Authentication service for business logic operations.
"""

from typing import Dict, Any, Optional
from datetime import datetime

from app.core.security import (
    create_employee_token, verify_token, get_current_user_payload,
    check_admin_role, require_admin
)
from app.core.exceptions import (
    AuthenticationException, AuthorizationException,
    FaceRecognitionException
)
from app.models.employee_model import Employee
from app.services.face_service import FaceService
from app.services.employee_service import EmployeeService
from app.services.attendance_service import AttendanceService


class AuthService:
    """Service for authentication operations."""
    
    def __init__(self):
        self.face_service = FaceService()
        self.employee_service = EmployeeService()
        self.attendance_service = AttendanceService()
    
    async def login_with_face(self, face_image: str) -> Dict[str, Any]:
        """Authenticate user using face recognition."""
        try:
            # Recognize face
            employee = await self.face_service.recognize_face(face_image)
            
            if not employee:
                raise AuthenticationException("Face recognition failed")
            
            # Create tokens
            tokens = create_employee_token(
                emp_id=employee.emp_id,
                name=employee.name,
                role=employee.role
            )
            
            # Mark attendance login
            try:
                await self.attendance_service.mark_attendance(employee.emp_id, "login")
            except Exception:
                # Don't fail login if attendance marking fails
                pass
            
            return {
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"],
                "token_type": tokens["token_type"],
                "expires_in": tokens["expires_in"],
                "user": {
                    "emp_id": employee.emp_id,
                    "name": employee.name,
                    "role": employee.role,
                    "email": employee.email,
                    "department": employee.department
                },
                "login_time": datetime.utcnow().isoformat()
            }
            
        except FaceRecognitionException as e:
            raise AuthenticationException(str(e))
        except Exception as e:
            raise AuthenticationException(f"Login failed: {str(e)}")
    
    async def logout_with_face(self, face_image: str, current_user: Dict[str, Any]) -> Dict[str, Any]:
        """Logout user using face verification."""
        try:
            # Verify face matches current user
            verification_result = await self.face_service.verify_face(face_image)
            
            if not verification_result["verified"]:
                raise AuthenticationException("Face verification failed")
            
            if verification_result["emp_id"] != current_user["sub"]:
                raise AuthenticationException("Face does not match current user")
            
            # Mark attendance logout
            try:
                attendance = await self.attendance_service.mark_attendance(
                    current_user["sub"], 
                    "logout"
                )
                
                return {
                    "emp_id": current_user["sub"],
                    "name": current_user["name"],
                    "logout_time": datetime.utcnow().isoformat(),
                    "total_hours": attendance.total_hours or 0
                }
            except Exception as e:
                # Return success even if attendance marking fails
                return {
                    "emp_id": current_user["sub"],
                    "name": current_user["name"],
                    "logout_time": datetime.utcnow().isoformat(),
                    "message": "Logout successful (attendance update failed)"
                }
            
        except AuthenticationException:
            raise
        except Exception as e:
            raise AuthenticationException(f"Logout failed: {str(e)}")
    
    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token using refresh token."""
        try:
            # Verify refresh token
            payload = verify_token(refresh_token, "refresh")
            
            # Get employee to ensure they still exist and are active
            employee = await self.employee_service.get_employee_by_id(payload["sub"])
            
            if not employee.is_active:
                raise AuthenticationException("Employee account is inactive")
            
            # Create new tokens
            tokens = create_employee_token(
                emp_id=employee.emp_id,
                name=employee.name,
                role=employee.role
            )
            
            return {
                "access_token": tokens["access_token"],
                "token_type": tokens["token_type"],
                "expires_in": tokens["expires_in"]
            }
            
        except AuthenticationException:
            raise
        except Exception as e:
            raise AuthenticationException(f"Token refresh failed: {str(e)}")
    
    async def authenticate_token(self, token: str) -> Dict[str, Any]:
        """Authenticate and validate JWT token."""
        try:
            # Verify token
            payload = get_current_user_payload(token)
            
            # Get employee to ensure they exist and are active
            employee = await self.employee_service.get_employee_by_id(payload["sub"])
            
            if not employee.is_active:
                raise AuthenticationException("Employee account is inactive")
            
            return {
                "emp_id": employee.emp_id,
                "name": employee.name,
                "role": employee.role,
                "email": employee.email,
                "department": employee.department,
                "last_login": employee.last_login
            }
            
        except AuthenticationException:
            raise
        except Exception as e:
            raise AuthenticationException(f"Token authentication failed: {str(e)}")
    
    async def authorize_admin(self, current_user: Dict[str, Any]) -> bool:
        """Check if current user has admin privileges."""
        try:
            if not check_admin_role(current_user):
                raise AuthorizationException("Admin access required")
            
            return True
            
        except AuthorizationException:
            raise
        except Exception as e:
            raise AuthorizationException(f"Authorization failed: {str(e)}")
    
    async def get_current_user_info(self, current_user: Dict[str, Any]) -> Dict[str, Any]:
        """Get current user information."""
        try:
            # Get full employee details
            employee = await self.employee_service.get_employee_by_id(current_user["sub"])
            
            # Get today's attendance if employee
            if employee.role == "employee":
                today_attendance = await self.attendance_service.get_today_attendance(employee.emp_id)
                
                return {
                    "emp_id": employee.emp_id,
                    "name": employee.name,
                    "email": employee.email,
                    "role": employee.role,
                    "department": employee.department,
                    "is_active": employee.is_active,
                    "has_face_encoding": employee.has_face_encoding(),
                    "last_login": employee.last_login,
                    "today_attendance": {
                        "is_logged_in": today_attendance.is_active_session() if today_attendance else False,
                        "login_time": today_attendance.login_time if today_attendance else None,
                        "logout_time": today_attendance.logout_time if today_attendance else None
                    } if today_attendance else None
                }
            else:
                # Admin user info
                employee_stats = await self.employee_service.get_employee_stats()
                attendance_stats = await self.attendance_service.get_attendance_stats()
                
                return {
                    "emp_id": employee.emp_id,
                    "name": employee.name,
                    "email": employee.email,
                    "role": employee.role,
                    "department": employee.department,
                    "is_active": employee.is_active,
                    "has_face_encoding": employee.has_face_encoding(),
                    "last_login": employee.last_login,
                    "admin_stats": {
                        "total_employees": employee_stats.get("total_employees", 0),
                        "present_today": attendance_stats.get("present_today", 0),
                        "absent_today": attendance_stats.get("absent_today", 0)
                    }
                }
            
        except Exception as e:
            raise AuthenticationException(f"Failed to get user info: {str(e)}")
    
    async def validate_face_registration_access(self, emp_id: str, current_user: Dict[str, Any]) -> bool:
        """Validate if current user can register face for given employee."""
        try:
            # Admin can register face for any employee
            if check_admin_role(current_user):
                return True
            
            # Employee can only register their own face
            if current_user["sub"] == emp_id:
                raise AuthorizationException("Cannot register face for your own account")
            
            # Register face
            face_service = employee_service.face_service if hasattr(employee_service, 'face_service') else None
            if not face_service:
                from app.services.face_service import FaceService
                face_service = FaceService()
        
            result = await face_service.register_face(emp_id, [face_image])
        
            return result
        
        except (NotFoundException, ValidationException) as e:
            raise
        except Exception as e:
            raise AuthorizationException(f"Face registration validation failed: {str(e)}")
    
    async def change_employee_role(self, emp_id: str, new_role: str, current_user: Dict[str, Any]) -> bool:
        """Change employee role (admin only)."""
        try:
            # Require admin access
            await self.authorize_admin(current_user)
            
            # Validate new role
            valid_roles = ["admin", "employee"]
            if new_role not in valid_roles:
                raise AuthorizationException(f"Invalid role. Must be one of: {valid_roles}")
            
            # Get target employee
            target_employee = await self.employee_service.get_employee_by_id(emp_id)
            
            # Prevent self-role modification for last admin
            if (target_employee.emp_id == current_user["sub"] and 
                target_employee.role == "admin" and 
                new_role != "admin"):
                
                # Check if this is the last admin
                admin_stats = await self.employee_service.get_employee_stats()
                admin_count = len([r for r in admin_stats.get("role_breakdown", []) 
                                 if r.get("role") == "admin"])
                
                if admin_count <= 1:
                    raise AuthorizationException("Cannot remove admin role from last admin")
            
            # Update employee role
            from app.models.employee_model import Employee
            from app.schemas.employee_schema import EmployeeUpdate
            update_data = EmployeeUpdate(role=new_role)
            await self.employee_service.update_employee(emp_id, update_data)
            
            return True
        
        except (AuthorizationException, AuthenticationException):
            raise
        except Exception as e:
            raise AuthorizationException(f"Role change failed: {str(e)}")
    
    async def deactivate_employee(self, emp_id: str, current_user: Dict[str, Any]) -> bool:
        """Deactivate employee account (admin only)."""
        try:
            # Require admin access
            await self.authorize_admin(current_user)
            
            # Prevent self-deactivation
            if emp_id == current_user["sub"]:
                raise AuthorizationException("Cannot deactivate your own account")
            
            # Get target employee
            target_employee = await self.employee_service.get_employee_by_id(emp_id)
            
            # Prevent deactivating last admin
            if target_employee.role == "admin":
                admin_stats = await self.employee_service.get_employee_stats()
                admin_count = len([r for r in admin_stats.get("role_breakdown", []) 
                                 if r.get("role") == "admin"])
                
                if admin_count <= 1:
                    raise AuthorizationException("Cannot deactivate last admin")
            
            # Deactivate employee
            await self.employee_service.delete_employee(emp_id)
            
            return True
            
        except (AuthorizationException, AuthenticationException):
            raise
        except Exception as e:
            raise AuthorizationException(f"Employee deactivation failed: {str(e)}")
