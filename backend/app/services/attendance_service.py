"""
Attendance service for business logic operations.
"""

from typing import List, Optional, Dict, Any, Tuple
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime, date, timedelta

from app.models.attendance_model import Attendance
from app.models.employee_model import Employee
from app.schemas.attendance_schema import AttendanceFilter
from app.core.exceptions import NotFoundException, DatabaseException
from app.database.mongodb import db
from app.services.employee_service import EmployeeService


class AttendanceService:
    """Service for attendance operations."""
    
    def __init__(self, database: AsyncIOMotorDatabase = None):
        self.database = database or db.get_database()
        self.collection = self.database.attendance
        self.employee_service = EmployeeService(database)
    
    async def mark_attendance(self, emp_id: str, attendance_type: str = "login") -> Attendance:
        """Mark employee attendance (login or logout)."""
        try:
            # Get employee
            employee = await self.employee_service.get_employee_by_id(emp_id)
            
            # Get today's date
            today = date.today()
            
            # Check if attendance record exists for today
            existing_record = await self.get_today_attendance(emp_id)
            
            if attendance_type == "login":
                if existing_record and existing_record.login_time:
                    raise DatabaseException(f"Employee {emp_id} has already logged in today")
                
                # Create new attendance record or update existing
                if existing_record:
                    existing_record.mark_login()
                    await self._update_attendance(existing_record.id, existing_record)
                    return existing_record
                else:
                    attendance = Attendance(
                        emp_id=emp_id,
                        date=today
                    )
                    attendance.mark_login()
                    
                    result = await self.collection.insert_one(attendance.to_mongo())
                    created_attendance = await self.get_attendance_by_id(str(result.inserted_id))
                    return created_attendance
            
            elif attendance_type == "logout":
                if not existing_record or not existing_record.login_time:
                    raise DatabaseException(f"Employee {emp_id} has not logged in today")
                
                if existing_record.logout_time:
                    raise DatabaseException(f"Employee {emp_id} has already logged out today")
                
                # Update existing record with logout time
                existing_record.mark_logout()
                await self._update_attendance(existing_record.id, existing_record)
                return existing_record
            
            else:
                raise DatabaseException("Invalid attendance type. Must be 'login' or 'logout'")
                
        except (NotFoundException, DatabaseException):
            raise
        except Exception as e:
            raise DatabaseException(f"Failed to mark attendance: {str(e)}")
    
    async def get_attendance_by_id(self, attendance_id: str) -> Attendance:
        """Get attendance record by ID."""
        try:
            if not ObjectId.is_valid(attendance_id):
                raise NotFoundException(f"Invalid attendance ID: {attendance_id}")
            
            attendance_doc = await self.collection.find_one({"_id": ObjectId(attendance_id)})
            if not attendance_doc:
                raise NotFoundException(f"Attendance record with ID {attendance_id} not found")
            
            attendance = Attendance.from_mongo(attendance_doc)
            
            # Add employee name if needed
            if not attendance.name:
                employee = await self.employee_service.get_employee_by_id(attendance.emp_id)
                attendance.name = employee.name
            
            return attendance
            
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Failed to get attendance record: {str(e)}")
    
    async def get_today_attendance(self, emp_id: str = None) -> Optional[Attendance]:
        """Get today's attendance for employee or all employees."""
        try:
            today = date.today()
            query = {"date": today}
            
            if emp_id:
                query["emp_id"] = emp_id
            
            attendance_doc = await self.collection.find_one(query)
            if attendance_doc:
                attendance = Attendance.from_mongo(attendance_doc)
                
                # Add employee name
                if not attendance.name:
                    employee = await self.employee_service.get_employee_by_id(attendance.emp_id)
                    attendance.name = employee.name
                
                return attendance
            
            return None
            
        except Exception as e:
            raise DatabaseException(f"Failed to get today's attendance: {str(e)}")
    
    async def get_attendance_records(self, filters: AttendanceFilter = None) -> Tuple[List[Attendance], Dict[str, Any]]:
        """Get attendance records with filtering and pagination."""
        try:
            # Build query
            query = {}
            
            if filters:
                if filters.emp_id:
                    query["emp_id"] = filters.emp_id
                
                if filters.date_from:
                    query["date"] = {"$gte": filters.date_from}
                
                if filters.date_to:
                    if "date" in query:
                        query["date"]["$lte"] = filters.date_to
                    else:
                        query["date"] = {"$lte": filters.date_to}
                
                if filters.status:
                    query["status"] = filters.status
            
            # Pagination
            page = filters.page if filters else 1
            limit = filters.limit if filters else 10
            skip = (page - 1) * limit
            
            # Get total count
            total = await self.collection.count_documents(query)
            
            # Get attendance records
            cursor = self.collection.find(query).skip(skip).limit(limit).sort("date", -1)
            attendance_records = []
            
            async for attendance_doc in cursor:
                attendance = Attendance.from_mongo(attendance_doc)
                
                # Add employee name
                if not attendance.name:
                    employee = await self.employee_service.get_employee_by_id(attendance.emp_id)
                    attendance.name = employee.name
                
                attendance_records.append(attendance)
            
            # Pagination info
            pages = (total + limit - 1) // limit
            pagination = {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": pages,
                "has_next": page < pages,
                "has_prev": page > 1
            }
            
            return attendance_records, pagination
            
        except Exception as e:
            raise DatabaseException(f"Failed to get attendance records: {str(e)}")
    
    async def get_today_all_attendance(self) -> Tuple[List[Attendance], Dict[str, Any]]:
        """Get today's attendance for all employees."""
        try:
            today = date.today()
            query = {"date": today}
            
            cursor = self.collection.find(query).sort("login_time", -1)
            attendance_records = []
            
            async for attendance_doc in cursor:
                attendance = Attendance.from_mongo(attendance_doc)
                
                # Add employee name
                if not attendance.name:
                    employee = await self.employee_service.get_employee_by_id(attendance.emp_id)
                    attendance.name = employee.name
                
                attendance_records.append(attendance)
            
            # Calculate summary
            total_present = len([r for r in attendance_records if r.status == "present"])
            total_absent = len([r for r in attendance_records if r.status == "absent"])
            total_active = len([r for r in attendance_records if r.is_active_session()])
            
            summary = {
                "total_present": total_present,
                "total_absent": total_absent,
                "total_active": total_active
            }
            
            return attendance_records, summary
            
        except Exception as e:
            raise DatabaseException(f"Failed to get today's attendance: {str(e)}")
    
    async def get_employee_attendance_history(self, emp_id: str, days: int = 30) -> Tuple[List[Attendance], Dict[str, Any]]:
        """Get attendance history for specific employee."""
        try:
            # Validate employee exists
            await self.employee_service.get_employee_by_id(emp_id)
            
            # Calculate date range
            end_date = date.today()
            start_date = end_date - timedelta(days=days)
            
            query = {
                "emp_id": emp_id,
                "date": {"$gte": start_date, "$lte": end_date}
            }
            
            cursor = self.collection.find(query).sort("date", -1)
            attendance_records = []
            
            async for attendance_doc in cursor:
                attendance = Attendance.from_mongo(attendance_doc)
                attendance_records.append(attendance)
            
            # Calculate summary
            total_days = len(attendance_records)
            present_days = len([r for r in attendance_records if r.status == "present"])
            absent_days = len([r for r in attendance_records if r.status == "absent"])
            total_hours = sum([r.total_hours or 0 for r in attendance_records])
            average_hours = total_hours / present_days if present_days > 0 else 0
            
            summary = {
                "total_days": total_days,
                "present_days": present_days,
                "absent_days": absent_days,
                "total_hours": round(total_hours, 2),
                "average_hours": round(average_hours, 2)
            }
            
            return attendance_records, summary
            
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Failed to get employee attendance history: {str(e)}")
    
    async def get_attendance_stats(self, period: str = "month") -> Dict[str, Any]:
        """Get attendance statistics for the specified period."""
        try:
            # Calculate date range based on period
            end_date = date.today()
            
            if period == "week":
                start_date = end_date - timedelta(days=7)
            elif period == "month":
                start_date = end_date - timedelta(days=30)
            elif period == "year":
                start_date = end_date - timedelta(days=365)
            else:
                start_date = end_date - timedelta(days=30)  # Default to month
            
            # Get employee stats
            employee_stats = await self.employee_service.get_employee_stats()
            total_employees = employee_stats.get("total_employees", 0)
            
            # Get today's attendance
            today_records, today_summary = await self.get_today_all_attendance()
            present_today = today_summary.get("total_present", 0)
            absent_today = today_summary.get("total_absent", 0)
            
            # Calculate average attendance rate
            pipeline = [
                {
                    "$match": {
                        "date": {"$gte": start_date, "$lte": end_date}
                    }
                },
                {
                    "$group": {
                        "_id": "$date",
                        "present": {
                            "$sum": {"$cond": [{"$eq": ["$status", "present"]}, 1, 0]}
                        },
                        "absent": {
                            "$sum": {"$cond": [{"$eq": ["$status", "absent"]}, 1, 0]}
                        }
                    }
                },
                {"$sort": {"_id": 1}}
            ]
            
            cursor = self.collection.aggregate(pipeline)
            daily_breakdown = await cursor.to_list(length=None)
            
            # Calculate average attendance rate
            total_possible = len(daily_breakdown) * total_employees
            total_present_sum = sum([day.get("present", 0) for day in daily_breakdown])
            average_attendance_rate = (total_present_sum / total_possible * 100) if total_possible > 0 else 0
            
            # Department breakdown (simplified - would need employee join)
            department_breakdown = []
            for role_stat in employee_stats.get("role_breakdown", []):
                department_breakdown.append({
                    "department": role_stat.get("role", "Unknown"),
                    "employees": role_stat.get("count", 0),
                    "attendance_rate": round(average_attendance_rate, 1)  # Simplified
                })
            
            return {
                "period": period,
                "total_employees": total_employees,
                "present_today": present_today,
                "absent_today": absent_today,
                "average_attendance_rate": round(average_attendance_rate, 1),
                "daily_breakdown": daily_breakdown,
                "department_breakdown": department_breakdown
            }
            
        except Exception as e:
            raise DatabaseException(f"Failed to get attendance stats: {str(e)}")
    
    async def export_attendance_to_csv(self, date_from: date = None, date_to: date = None, emp_id: str = None) -> List[Dict[str, Any]]:
        """Export attendance data for CSV generation."""
        try:
            # Build query
            query = {}
            
            if emp_id:
                query["emp_id"] = emp_id
            
            if date_from or date_to:
                date_query = {}
                if date_from:
                    date_query["$gte"] = date_from
                if date_to:
                    date_query["$lte"] = date_to
                query["date"] = date_query
            
            # Get attendance records
            cursor = self.collection.find(query).sort("date", -1)
            export_data = []
            
            async for attendance_doc in cursor:
                attendance = Attendance.from_mongo(attendance_doc)
                
                # Get employee name
                employee = await self.employee_service.get_employee_by_id(attendance.emp_id)
                
                export_data.append({
                    "Employee ID": attendance.emp_id,
                    "Name": employee.name,
                    "Date": attendance.date,
                    "Login Time": attendance.login_time or "",
                    "Logout Time": attendance.logout_time or "",
                    "Total Hours": attendance.total_hours or 0,
                    "Status": attendance.status,
                    "Duration": attendance.get_duration() or ""
                })
            
            return export_data
            
        except Exception as e:
            raise DatabaseException(f"Failed to export attendance data: {str(e)}")
    
    async def _update_attendance(self, attendance_id: str, attendance: Attendance) -> None:
        """Update attendance record in database."""
        try:
            if not ObjectId.is_valid(attendance_id):
                raise NotFoundException(f"Invalid attendance ID: {attendance_id}")
            
            await self.collection.update_one(
                {"_id": ObjectId(attendance_id)},
                {"$set": attendance.to_mongo()}
            )
            
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Failed to update attendance: {str(e)}")
