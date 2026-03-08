"""
Attendance management router.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from typing import List
from datetime import date
import csv
import io

from app.schemas.attendance_schema import (
    AttendanceResponse, AttendanceListResponse, 
    AttendanceFilter, TodayAttendanceResponse,
    AttendanceStatsResponse, EmployeeAttendanceHistory
)
from app.schemas.response_schema import SuccessResponse
from app.services.attendance_service import AttendanceService
from app.services.auth_service import AuthService
from app.dependencies.auth_dependency import get_current_user
from app.core.exceptions import (
    NotFoundException, DatabaseException, ValidationException
)

router = APIRouter(prefix="/attendance", tags=["attendance"])
attendance_service = AttendanceService()
auth_service = AuthService()


@router.get("/", response_model=AttendanceListResponse)
async def get_attendance(
    filters: AttendanceFilter = AttendanceFilter(),
    current_user: dict = Depends(get_current_user)
):
    """Get attendance records with filtering and pagination."""
    try:
        # Employees can only see their own attendance
        if current_user["role"] != "admin":
            filters.emp_id = current_user["sub"]
        
        attendance_records, pagination = await attendance_service.get_attendance_records(filters)
        
        attendance_responses = [
            AttendanceResponse(
                id=str(record.id),
                emp_id=record.emp_id,
                name=record.name,
                date=record.date,
                login_time=record.login_time,
                logout_time=record.logout_time,
                total_hours=record.total_hours,
                status=record.status,
                created_at=record.created_at,
                updated_at=record.updated_at,
                duration=record.get_duration(),
                is_active_session=record.is_active_session()
            )
            for record in attendance_records
        ]
        
        return AttendanceListResponse(
            attendance=attendance_responses,
            pagination=pagination
        )
        
    except (NotFoundException, ValidationException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/today", response_model=TodayAttendanceResponse)
async def get_today_attendance(
    current_user: dict = Depends(get_current_user)
):
    """Get today's attendance records."""
    try:
        # Employees can only see their own attendance
        if current_user["role"] == "employee":
            today_record = await attendance_service.get_today_attendance(current_user["sub"])
            records = [today_record] if today_record else []
            summary = {
                "total_present": 1 if today_record and today_record.login_time else 0,
                "total_absent": 0 if today_record and today_record.login_time else 1,
                "total_active": 1 if today_record and today_record.is_active_session() else 0
            }
        else:
            # Admin can see all today's attendance
            records, summary = await attendance_service.get_today_all_attendance()
        
        attendance_responses = [
            AttendanceResponse(
                id=str(record.id),
                emp_id=record.emp_id,
                name=record.name,
                date=record.date,
                login_time=record.login_time,
                logout_time=record.logout_time,
                total_hours=record.total_hours,
                status=record.status,
                created_at=record.created_at,
                updated_at=record.updated_at,
                duration=record.get_duration(),
                is_active_session=record.is_active_session()
            )
            for record in records
        ]
        
        return TodayAttendanceResponse(
            date=date.today(),
            records=attendance_responses,
            summary=summary
        )
        
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/date/{attendance_date}", response_model=TodayAttendanceResponse)
async def get_attendance_by_date(
    attendance_date: date,
    current_user: dict = Depends(get_current_user)
):
    """Get attendance for specific date."""
    try:
        # Build filters
        filters = AttendanceFilter(
            date_from=attendance_date,
            date_to=attendance_date
        )
        
        # Employees can only see their own attendance
        if current_user["role"] != "admin":
            filters.emp_id = current_user["sub"]
        
        attendance_records, pagination = await attendance_service.get_attendance_records(filters)
        
        attendance_responses = [
            AttendanceResponse(
                id=str(record.id),
                emp_id=record.emp_id,
                name=record.name,
                date=record.date,
                login_time=record.login_time,
                logout_time=record.logout_time,
                total_hours=record.total_hours,
                status=record.status,
                created_at=record.created_at,
                updated_at=record.updated_at,
                duration=record.get_duration(),
                is_active_session=record.is_active_session()
            )
            for record in attendance_records
        ]
        
        # Calculate summary
        total_present = len([r for r in attendance_responses if r.status == "present"])
        total_absent = len([r for r in attendance_responses if r.status == "absent"])
        total_hours = sum([r.total_hours or 0 for r in attendance_responses])
        
        summary = {
            "total_present": total_present,
            "total_absent": total_absent,
            "total_hours": round(total_hours, 2)
        }
        
        return TodayAttendanceResponse(
            date=attendance_date,
            records=attendance_responses,
            summary=summary
        )
        
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/employee/{emp_id}", response_model=EmployeeAttendanceHistory)
async def get_employee_attendance_history(
    emp_id: str,
    days: int = 30,
    current_user: dict = Depends(get_current_user)
):
    """Get attendance history for specific employee."""
    try:
        # Employees can only see their own attendance
        if current_user["role"] != "admin" and current_user["sub"] != emp_id:
            raise ValidationException("Not authorized to view this employee's attendance")
        
        attendance_records, summary = await attendance_service.get_employee_attendance_history(emp_id, days)
        
        attendance_responses = [
            AttendanceResponse(
                id=str(record.id),
                emp_id=record.emp_id,
                name=record.name,
                date=record.date,
                login_time=record.login_time,
                logout_time=record.logout_time,
                total_hours=record.total_hours,
                status=record.status,
                created_at=record.created_at,
                updated_at=record.updated_at,
                duration=record.get_duration(),
                is_active_session=record.is_active_session()
            )
            for record in attendance_records
        ]
        
        # Get employee name
        employee_service = attendance_service.employee_service
        employee = await employee_service.get_employee_by_id(emp_id)
        
        return EmployeeAttendanceHistory(
            emp_id=emp_id,
            name=employee.name,
            records=attendance_responses,
            summary=summary
        )
        
    except (NotFoundException, ValidationException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/stats/summary", response_model=AttendanceStatsResponse)
async def get_attendance_stats(
    period: str = "month",
    current_user: dict = Depends(get_current_user)
):
    """Get attendance statistics (admin only)."""
    try:
        # Require admin access
        await auth_service.authorize_admin(current_user)
        
        stats = await attendance_service.get_attendance_stats(period)
        
        return AttendanceStatsResponse(**stats)
        
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/export")
async def export_attendance_csv(
    date_from: date = None,
    date_to: date = None,
    emp_id: str = None,
    current_user: dict = Depends(get_current_user)
):
    """Export attendance data to CSV (admin only)."""
    try:
        # Require admin access
        await auth_service.authorize_admin(current_user)
        
        # Employees can only export their own data
        if current_user["role"] != "admin":
            emp_id = current_user["sub"]
        
        # Get export data
        export_data = await attendance_service.export_attendance_to_csv(date_from, date_to, emp_id)
        
        if not export_data:
            raise ValidationException("No data found for export")
        
        # Create CSV
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=export_data[0].keys())
        writer.writeheader()
        writer.writerows(export_data)
        
        # Generate filename
        filename = f"attendance_export_{date.today()}.csv"
        
        # Return CSV response
        response = StreamingResponse(
            io.StringIO(output.getvalue()),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
        return response
        
    except (ValidationException, NotFoundException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/mark/{attendance_type}")
async def mark_attendance(
    attendance_type: str,
    current_user: dict = Depends(get_current_user)
):
    """Mark attendance for current user (login/logout)."""
    try:
        # Only employees can mark their own attendance
        if current_user["role"] != "employee":
            raise ValidationException("Only employees can mark attendance")
        
        if attendance_type not in ["login", "logout"]:
            raise ValidationException("Attendance type must be 'login' or 'logout'")
        
        # Mark attendance
        attendance = await attendance_service.mark_attendance(current_user["sub"], attendance_type)
        
        return SuccessResponse(
            data={
                "emp_id": attendance.emp_id,
                "date": attendance.date,
                "login_time": attendance.login_time,
                "logout_time": attendance.logout_time,
                "total_hours": attendance.total_hours,
                "status": attendance.status
            },
            message=f"Attendance {attendance_type} marked successfully"
        )
        
    except (ValidationException, DatabaseException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
