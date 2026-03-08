"""
Authentication router.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any

from app.schemas.auth_schema import (
    RefreshTokenRequest, TokenResponse, LoginResponse
)
from app.schemas.response_schema import SuccessResponse
from app.services.auth_service import AuthService
from app.core.exceptions import AuthenticationException, ValidationException, DatabaseException

router = APIRouter(prefix="/auth", tags=["authentication"])
auth_service = AuthService()
security = HTTPBearer()


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_request: RefreshTokenRequest):
    """Refresh access token using refresh token."""
    try:
        token_data = await auth_service.refresh_token(refresh_request.refresh_token)
        
        return TokenResponse(
            access_token=token_data["access_token"],
            token_type=token_data["token_type"],
            expires_in=token_data["expires_in"]
        )
        
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/me")
async def get_current_user_info(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get current user information."""
    try:
        # Authenticate token
        user_info = await auth_service.authenticate_token(credentials.credentials)
        
        return SuccessResponse(
            data=user_info,
            message="User information retrieved successfully"
        )
        
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Logout user (invalidate token)."""
    try:
        # Authenticate token
        user_info = await auth_service.authenticate_token(credentials.credentials)
        
        # In a production environment, you would:
        # 1. Add the token to a blacklist
        # 2. Remove the refresh token from the database
        # 3. Clear any session data
        
        return SuccessResponse(
            data={"emp_id": user_info["emp_id"], "name": user_info["name"]},
            message="Logout successful"
        )
        
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/validate")
async def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Validate JWT token."""
    try:
        # Authenticate token
        user_info = await auth_service.authenticate_token(credentials.credentials)
        
        return SuccessResponse(
            data={
                "valid": True,
                "emp_id": user_info["emp_id"],
                "role": user_info["role"]
            },
            message="Token is valid"
        )
        
    except AuthenticationException as e:
        return SuccessResponse(
            data={"valid": False},
            message=str(e)
        )
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/change-role/{emp_id}")
async def change_employee_role(
    emp_id: str,
    role_data: Dict[str, str],
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Change employee role (admin only)."""
    try:
        # Authenticate current user
        current_user = await auth_service.authenticate_token(credentials.credentials)
        
        # Change role
        success = await auth_service.change_employee_role(
            emp_id, 
            role_data.get("new_role", ""), 
            current_user
        )
        
        if success:
            return SuccessResponse(
                data={"emp_id": emp_id, "new_role": role_data.get("new_role")},
                message="Employee role changed successfully"
            )
        else:
            raise ValidationException("Failed to change employee role")
        
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/permissions")
async def get_user_permissions(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get current user permissions."""
    try:
        # Authenticate token
        user_info = await auth_service.authenticate_token(credentials.credentials)
        
        # Define permissions based on role
        permissions = {
            "emp_id": user_info["emp_id"],
            "role": user_info["role"],
            "permissions": []
        }
        
        if user_info["role"] == "admin":
            permissions["permissions"] = [
                "employee:read",
                "employee:write",
                "employee:delete",
                "attendance:read_all",
                "attendance:export",
                "face:register_all",
                "auth:change_role",
                "auth:deactivate_user"
            ]
        else:
            permissions["permissions"] = [
                "attendance:read_own",
                "face:register_own",
                "profile:read_own",
                "profile:update_own"
            ]
        
        return SuccessResponse(
            data=permissions,
            message="User permissions retrieved successfully"
        )
        
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/session-info")
async def get_session_info(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get detailed session information."""
    try:
        # Authenticate token
        user_info = await auth_service.authenticate_token(credentials.credentials)
        
        # Get detailed user info
        detailed_info = await auth_service.get_current_user_info(user_info)
        
        return SuccessResponse(
            data=detailed_info,
            message="Session information retrieved successfully"
        )
        
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
