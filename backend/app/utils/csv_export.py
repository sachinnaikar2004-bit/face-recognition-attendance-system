"""
CSV export utilities for attendance data.
"""

import csv
import io
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from fastapi.responses import StreamingResponse

from app.core.exceptions import DatabaseException


class CSVExportUtils:
    """Utilities for CSV export operations."""
    
    @staticmethod
    def create_csv_response(data: List[Dict[str, Any]], filename: str = None) -> StreamingResponse:
        """Create streaming CSV response from data."""
        try:
            if not data:
                raise DatabaseException("No data to export")
            
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"export_{timestamp}.csv"
            
            # Create CSV in memory
            output = io.StringIO()
            
            # Get headers from first row
            headers = list(data[0].keys())
            
            # Write CSV
            writer = csv.DictWriter(output, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
            
            # Create streaming response
            response = StreamingResponse(
                io.StringIO(output.getvalue()),
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
            
            return response
            
        except Exception as e:
            raise DatabaseException(f"Failed to create CSV response: {str(e)}")
    
    @staticmethod
    def export_attendance_data(attendance_records: List[Dict[str, Any]], 
                            date_from: date = None, date_to: date = None) -> List[Dict[str, Any]]:
        """Format attendance data for CSV export."""
        try:
            export_data = []
            
            for record in attendance_records:
                export_row = {
                    "Employee ID": record.get("emp_id", ""),
                    "Name": record.get("name", ""),
                    "Date": record.get("date", ""),
                    "Login Time": record.get("login_time", ""),
                    "Logout Time": record.get("logout_time", ""),
                    "Total Hours": record.get("total_hours", 0),
                    "Status": record.get("status", ""),
                    "Duration": record.get("duration", "")
                }
                export_data.append(export_row)
            
            # Sort by date and employee ID
            export_data.sort(key=lambda x: (x["Date"], x["Employee ID"]))
            
            return export_data
            
        except Exception as e:
            raise DatabaseException(f"Failed to format attendance data: {str(e)}")
    
    @staticmethod
    def export_employee_data(employees: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format employee data for CSV export."""
        try:
            export_data = []
            
            for employee in employees:
                export_row = {
                    "Employee ID": employee.get("emp_id", ""),
                    "Name": employee.get("name", ""),
                    "Email": employee.get("email", ""),
                    "Role": employee.get("role", ""),
                    "Department": employee.get("department", ""),
                    "Active": "Yes" if employee.get("is_active", False) else "No",
                    "Has Face Encoding": "Yes" if employee.get("has_face_encoding", False) else "No",
                    "Created Date": employee.get("created_at", ""),
                    "Last Login": employee.get("last_login", "")
                }
                export_data.append(export_row)
            
            # Sort by employee ID
            export_data.sort(key=lambda x: x["Employee ID"])
            
            return export_data
            
        except Exception as e:
            raise DatabaseException(f"Failed to format employee data: {str(e)}")
    
    @staticmethod
    def export_attendance_summary(attendance_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create attendance summary for CSV export."""
        try:
            # Calculate summary statistics
            summary_data = []
            
            # Total records
            total_records = len(attendance_data)
            summary_data.append({
                "Metric": "Total Attendance Records",
                "Value": total_records
            })
            
            # Present days
            present_days = len([r for r in attendance_data if r.get("status") == "present"])
            summary_data.append({
                "Metric": "Present Days",
                "Value": present_days
            })
            
            # Absent days
            absent_days = len([r for r in attendance_data if r.get("status") == "absent"])
            summary_data.append({
                "Metric": "Absent Days",
                "Value": absent_days
            })
            
            # Total hours
            total_hours = sum([r.get("total_hours", 0) for r in attendance_data])
            summary_data.append({
                "Metric": "Total Work Hours",
                "Value": round(total_hours, 2)
            })
            
            # Average hours per day
            if present_days > 0:
                avg_hours = total_hours / present_days
                summary_data.append({
                    "Metric": "Average Hours Per Day",
                    "Value": round(avg_hours, 2)
                })
            
            # Unique employees
            unique_employees = len(set([r.get("emp_id") for r in attendance_data]))
            summary_data.append({
                "Metric": "Unique Employees",
                "Value": unique_employees
            })
            
            return summary_data
            
        except Exception as e:
            raise DatabaseException(f"Failed to create attendance summary: {str(e)}")
    
    @staticmethod
    def create_monthly_report(attendance_data: List[Dict[str, Any]], 
                            month: int, year: int) -> List[Dict[str, Any]]:
        """Create monthly attendance report."""
        try:
            # Filter data for specified month
            monthly_data = []
            
            for record in attendance_data:
                record_date = record.get("date")
                if isinstance(record_date, str):
                    record_date = datetime.strptime(record_date, "%Y-%m-%d").date()
                
                if record_date.month == month and record_date.year == year:
                    monthly_data.append(record)
            
            # Group by employee
            employee_monthly = {}
            for record in monthly_data:
                emp_id = record.get("emp_id")
                if emp_id not in employee_monthly:
                    employee_monthly[emp_id] = {
                        "Employee ID": emp_id,
                        "Name": record.get("name", ""),
                        "Month": f"{year}-{month:02d}",
                        "Present Days": 0,
                        "Absent Days": 0,
                        "Total Hours": 0,
                        "Average Hours": 0,
                        "Late Arrivals": 0,
                        "Early Departures": 0
                    }
                
                emp_data = employee_monthly[emp_id]
                
                if record.get("status") == "present":
                    emp_data["Present Days"] += 1
                    emp_data["Total Hours"] += record.get("total_hours", 0)
                    
                    # Check for late arrival (after 9:00 AM)
                    login_time = record.get("login_time")
                    if login_time:
                        try:
                            login_dt = datetime.strptime(login_time, "%H:%M:%S")
                            if login_dt.hour > 9 or (login_dt.hour == 9 and login_dt.minute > 0):
                                emp_data["Late Arrivals"] += 1
                        except ValueError:
                            pass
                    
                    # Check for early departure (before 5:00 PM)
                    logout_time = record.get("logout_time")
                    if logout_time:
                        try:
                            logout_dt = datetime.strptime(logout_time, "%H:%M:%S")
                            if logout_dt.hour < 17 or (logout_dt.hour == 17 and logout_dt.minute < 30):
                                emp_data["Early Departures"] += 1
                        except ValueError:
                            pass
                else:
                    emp_data["Absent Days"] += 1
            
            # Calculate averages
            for emp_data in employee_monthly.values():
                if emp_data["Present Days"] > 0:
                    emp_data["Average Hours"] = round(emp_data["Total Hours"] / emp_data["Present Days"], 2)
            
            return list(employee_monthly.values())
            
        except Exception as e:
            raise DatabaseException(f"Failed to create monthly report: {str(e)}")
    
    @staticmethod
    def validate_export_data(data: List[Dict[str, Any]]) -> bool:
        """Validate data for export."""
        try:
            if not data:
                return False
            
            # Check if all rows have the same structure
            if len(data) > 1:
                first_keys = set(data[0].keys())
                for row in data[1:]:
                    if set(row.keys()) != first_keys:
                        return False
            
            return True
            
        except Exception:
            return False
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe file download."""
        try:
            # Remove or replace unsafe characters
            unsafe_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
            sanitized = filename
            
            for char in unsafe_chars:
                sanitized = sanitized.replace(char, '_')
            
            # Remove leading/trailing spaces and dots
            sanitized = sanitized.strip(' .')
            
            # Ensure filename is not empty
            if not sanitized:
                sanitized = "export"
            
            # Add .csv extension if not present
            if not sanitized.lower().endswith('.csv'):
                sanitized += '.csv'
            
            return sanitized
            
        except Exception:
            return "export.csv"
