"""
Employee service for business logic operations.
"""

from typing import List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime

from app.models.employee_model import Employee
from app.schemas.employee_schema import EmployeeCreate, EmployeeUpdate, EmployeeSearchFilter
from app.core.exceptions import (
    NotFoundException, DuplicateResourceException, 
    DatabaseException, ValidationException
)
from app.database.mongodb import db


class EmployeeService:
    """Service for employee operations."""
    
    def __init__(self, database: AsyncIOMotorDatabase = None):
        self.database = database or db.get_database()
        self.collection = self.database.employees
    
    async def create_employee(self, employee_data: EmployeeCreate) -> Employee:
        """Create a new employee."""
        try:
            # Check if employee ID already exists
            existing_emp = await self.collection.find_one({"emp_id": employee_data.emp_id})
            if existing_emp:
                raise DuplicateResourceException(f"Employee with ID {employee_data.emp_id} already exists")
            
            # Check if email already exists
            existing_email = await self.collection.find_one({"email": employee_data.email})
            if existing_email:
                raise DuplicateResourceException(f"Employee with email {employee_data.email} already exists")
            
            # Create employee document
            employee = Employee(
                emp_id=employee_data.emp_id,
                name=employee_data.name,
                email=employee_data.email,
                role=employee_data.role,
                department=employee_data.department
            )
            
            # Insert into database
            result = await self.collection.insert_one(employee.to_mongo())
            
            # Get the created employee
            created_employee = await self.get_employee_by_id(str(result.inserted_id))
            return created_employee
            
        except DuplicateResourceException:
            raise
        except Exception as e:
            raise DatabaseException(f"Failed to create employee: {str(e)}")
    
    async def get_employee_by_id(self, employee_id: str) -> Employee:
        """Get employee by ID."""
        try:
            # Convert string ID to ObjectId if needed
            if ObjectId.is_valid(employee_id):
                employee_doc = await self.collection.find_one({"_id": ObjectId(employee_id)})
            else:
                employee_doc = await self.collection.find_one({"emp_id": employee_id})
            
            if not employee_doc:
                raise NotFoundException(f"Employee with ID {employee_id} not found")
            
            return Employee.from_mongo(employee_doc)
            
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Failed to get employee: {str(e)}")
    
    async def get_employees(self, filters: EmployeeSearchFilter = None) -> tuple[List[Employee], Dict[str, Any]]:
        """Get employees with optional filtering and pagination."""
        try:
            # Build query
            query = {"is_active": True}
            
            if filters:
                if filters.search:
                    search_term = filters.search
                    query["$or"] = [
                        {"name": {"$regex": search_term, "$options": "i"}},
                        {"emp_id": {"$regex": search_term, "$options": "i"}}
                    ]
                
                if filters.role:
                    query["role"] = filters.role
                
                if filters.department:
                    query["department"] = {"$regex": filters.department, "$options": "i"}
                
                if filters.is_active is not None:
                    query["is_active"] = filters.is_active
            
            # Pagination
            page = filters.page if filters else 1
            limit = filters.limit if filters else 10
            skip = (page - 1) * limit
            
            # Get total count
            total = await self.collection.count_documents(query)
            
            # Get employees
            cursor = self.collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
            employees = []
            
            async for employee_doc in cursor:
                employees.append(Employee.from_mongo(employee_doc))
            
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
            
            return employees, pagination
            
        except Exception as e:
            raise DatabaseException(f"Failed to get employees: {str(e)}")
    
    async def update_employee(self, employee_id: str, update_data: EmployeeUpdate) -> Employee:
        """Update employee information."""
        try:
            # Get existing employee
            employee = await self.get_employee_by_id(employee_id)
            
            # Prepare update data
            update_dict = {}
            for field, value in update_data.dict(exclude_unset=True).items():
                if field != "face_image":  # Handle face image separately
                    update_dict[field] = value
            
            # Handle email uniqueness check
            if "email" in update_dict and update_dict["email"] != employee.email:
                existing_email = await self.collection.find_one({
                    "email": update_dict["email"],
                    "_id": {"$ne": ObjectId(employee.id) if ObjectId.is_valid(employee.id) else None}
                })
                if existing_email:
                    raise DuplicateResourceException(f"Email {update_dict['email']} is already in use")
            
            # Add updated timestamp
            update_dict["updated_at"] = datetime.utcnow()
            
            # Update in database
            if ObjectId.is_valid(employee.id):
                await self.collection.update_one(
                    {"_id": ObjectId(employee.id)},
                    {"$set": update_dict}
                )
            else:
                await self.collection.update_one(
                    {"emp_id": employee_id},
                    {"$set": update_dict}
                )
            
            # Return updated employee
            return await self.get_employee_by_id(employee_id)
            
        except (NotFoundException, DuplicateResourceException):
            raise
        except Exception as e:
            raise DatabaseException(f"Failed to update employee: {str(e)}")
    
    async def delete_employee(self, employee_id: str) -> bool:
        """Delete employee (soft delete)."""
        try:
            # Get existing employee
            employee = await self.get_employee_by_id(employee_id)
            
            # Soft delete by setting is_active to False
            if ObjectId.is_valid(employee.id):
                result = await self.collection.update_one(
                    {"_id": ObjectId(employee.id)},
                    {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
                )
            else:
                result = await self.collection.update_one(
                    {"emp_id": employee_id},
                    {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
                )
            
            return result.modified_count > 0
            
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Failed to delete employee: {str(e)}")
    
    async def update_face_encoding(self, employee_id: str, face_encoding: List[float]) -> Employee:
        """Update employee face encoding."""
        try:
            # Validate face encoding
            if len(face_encoding) != 128:
                raise ValidationException("Face encoding must be 128-dimensional")
            
            # Get existing employee
            employee = await self.get_employee_by_id(employee_id)
            
            # Update face encoding
            update_dict = {
                "face_encoding": face_encoding,
                "updated_at": datetime.utcnow()
            }
            
            if ObjectId.is_valid(employee.id):
                await self.collection.update_one(
                    {"_id": ObjectId(employee.id)},
                    {"$set": update_dict}
                )
            else:
                await self.collection.update_one(
                    {"emp_id": employee_id},
                    {"$set": update_dict}
                )
            
            return await self.get_employee_by_id(employee_id)
            
        except (NotFoundException, ValidationException):
            raise
        except Exception as e:
            raise DatabaseException(f"Failed to update face encoding: {str(e)}")
    
    async def get_employees_with_face_encoding(self) -> List[Employee]:
        """Get all employees who have face encoding."""
        try:
            query = {
                "is_active": True,
                "face_encoding": {"$exists": True, "$ne": []}
            }
            
            cursor = self.collection.find(query).sort("created_at", -1)
            employees = []
            
            async for employee_doc in cursor:
                employees.append(Employee.from_mongo(employee_doc))
            
            return employees
            
        except Exception as e:
            raise DatabaseException(f"Failed to get employees with face encoding: {str(e)}")
    
    async def update_last_login(self, employee_id: str) -> None:
        """Update employee last login timestamp."""
        try:
            update_dict = {"last_login": datetime.utcnow()}
            
            if ObjectId.is_valid(employee_id):
                await self.collection.update_one(
                    {"_id": ObjectId(employee_id)},
                    {"$set": update_dict}
                )
            else:
                await self.collection.update_one(
                    {"emp_id": employee_id},
                    {"$set": update_dict}
                )
                
        except Exception as e:
            raise DatabaseException(f"Failed to update last login: {str(e)}")
    
    async def get_employee_stats(self) -> Dict[str, Any]:
        """Get employee statistics."""
        try:
            pipeline = [
                {"$match": {"is_active": True}},
                {"$group": {
                    "_id": "$role",
                    "count": {"$sum": 1}
                }},
                {"$group": {
                    "_id": None,
                    "total": {"$sum": "$count"},
                    "roles": {
                        "$push": {
                            "role": "$_id",
                            "count": "$count"
                        }
                    }
                }}
            ]
            
            cursor = self.collection.aggregate(pipeline)
            result = await cursor.to_list(length=1)
            
            if result:
                stats = result[0]
                return {
                    "total_employees": stats.get("total", 0),
                    "role_breakdown": stats.get("roles", [])
                }
            else:
                return {
                    "total_employees": 0,
                    "role_breakdown": []
                }
                
        except Exception as e:
            raise DatabaseException(f"Failed to get employee stats: {str(e)}")
