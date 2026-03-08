# API Design Documentation

## Base Configuration
- **Base URL**: `http://localhost:8000/api/v1`
- **Content-Type**: `application/json`
- **Authentication**: Bearer Token (JWT)
- **CORS**: Enabled for frontend domain

## Authentication Endpoints

### POST /auth/login
**Purpose**: Authenticate user with face recognition
**Request**:
```json
{
  "face_image": "base64_encoded_image_string"
}
```
**Response**:
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer",
    "expires_in": 3600,
    "user": {
      "emp_id": "EMP001",
      "name": "John Doe",
      "role": "employee"
    }
  },
  "message": "Login successful"
}
```

### POST /auth/logout
**Purpose**: Logout user and invalidate token
**Headers**: `Authorization: Bearer <token>`
**Response**:
```json
{
  "success": true,
  "message": "Logout successful"
}
```

### POST /auth/refresh
**Purpose**: Refresh access token
**Request**:
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
**Response**:
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "expires_in": 3600
  }
}
```

## Employee Management Endpoints

### GET /employees
**Purpose**: Get all employees (Admin only)
**Headers**: `Authorization: Bearer <token>`
**Query Parameters**:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)
- `search`: Search by name or emp_id
- `role`: Filter by role

**Response**:
```json
{
  "success": true,
  "data": {
    "employees": [
      {
        "emp_id": "EMP001",
        "name": "John Doe",
        "email": "john@example.com",
        "role": "employee",
        "department": "Engineering",
        "created_at": "2024-01-01T00:00:00Z",
        "last_login": "2024-01-15T09:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 25,
      "pages": 3
    }
  }
}
```

### POST /employees
**Purpose**: Add new employee (Admin only)
**Headers**: `Authorization: Bearer <token>`
**Request**:
```json
{
  "emp_id": "EMP002",
  "name": "Jane Smith",
  "email": "jane@example.com",
  "role": "employee",
  "department": "HR",
  "face_image": "base64_encoded_image_string"
}
```
**Response**:
```json
{
  "success": true,
  "data": {
    "emp_id": "EMP002",
    "name": "Jane Smith",
    "email": "jane@example.com",
    "role": "employee",
    "department": "HR",
    "created_at": "2024-01-01T00:00:00Z"
  },
  "message": "Employee created successfully"
}
```

### GET /employees/{id}
**Purpose**: Get specific employee details
**Headers**: `Authorization: Bearer <token>`
**Response**:
```json
{
  "success": true,
  "data": {
    "emp_id": "EMP001",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "employee",
    "department": "Engineering",
    "created_at": "2024-01-01T00:00:00Z",
    "last_login": "2024-01-15T09:00:00Z",
    "total_attendance_days": 15,
    "average_work_hours": 8.5
  }
}
```

### PUT /employees/{id}
**Purpose**: Update employee information (Admin only)
**Headers**: `Authorization: Bearer <token>`
**Request**:
```json
{
  "name": "John Doe Updated",
  "email": "john.doe@example.com",
  "department": "Product Engineering"
}
```
**Response**:
```json
{
  "success": true,
  "data": {
    "emp_id": "EMP001",
    "name": "John Doe Updated",
    "email": "john.doe@example.com",
    "department": "Product Engineering",
    "updated_at": "2024-01-15T10:00:00Z"
  },
  "message": "Employee updated successfully"
}
```

### DELETE /employees/{id}
**Purpose**: Delete employee (Admin only)
**Headers**: `Authorization: Bearer <token>`
**Response**:
```json
{
  "success": true,
  "message": "Employee deleted successfully"
}
```

### POST /employees/{id}/recapture-face
**Purpose**: Recapture employee face image (Admin only)
**Headers**: `Authorization: Bearer <token>`
**Request**:
```json
{
  "face_image": "base64_encoded_image_string"
}
```
**Response**:
```json
{
  "success": true,
  "message": "Face image updated successfully"
}
```

## Attendance Endpoints

### GET /attendance
**Purpose**: Get attendance records (Admin: all, Employee: own)
**Headers**: `Authorization: Bearer <token>`
**Query Parameters**:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)
- `date_from`: Start date (YYYY-MM-DD)
- `date_to`: End date (YYYY-MM-DD)
- `emp_id`: Filter by employee (Admin only)

**Response**:
```json
{
  "success": true,
  "data": {
    "attendance": [
      {
        "id": "64a1b2c3d4e5f6789012345",
        "emp_id": "EMP001",
        "name": "John Doe",
        "date": "2024-01-15",
        "login_time": "09:00:00",
        "logout_time": "17:30:00",
        "total_hours": 8.5,
        "status": "present"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 50,
      "pages": 5
    },
    "summary": {
      "total_records": 50,
      "total_hours": 425.5,
      "average_hours": 8.51
    }
  }
}
```

### GET /attendance/today
**Purpose**: Get today's attendance records
**Headers**: `Authorization: Bearer <token>`
**Response**:
```json
{
  "success": true,
  "data": {
    "date": "2024-01-15",
    "records": [
      {
        "emp_id": "EMP001",
        "name": "John Doe",
        "login_time": "09:00:00",
        "logout_time": null,
        "status": "active"
      }
    ],
    "summary": {
      "total_present": 15,
      "total_absent": 5,
      "total_active": 10
    }
  }
}
```

### GET /attendance/date/{date}
**Purpose**: Get attendance for specific date
**Headers**: `Authorization: Bearer <token>`
**Path Parameters**: `date` (YYYY-MM-DD)
**Response**:
```json
{
  "success": true,
  "data": {
    "date": "2024-01-15",
    "records": [
      {
        "emp_id": "EMP001",
        "name": "John Doe",
        "login_time": "09:00:00",
        "logout_time": "17:30:00",
        "total_hours": 8.5,
        "status": "present"
      }
    ],
    "summary": {
      "total_present": 20,
      "total_absent": 2,
      "total_hours": 170.5
    }
  }
}
```

### GET /attendance/employee/{id}
**Purpose**: Get attendance history for specific employee
**Headers**: `Authorization: Bearer <token>`
**Path Parameters**: `id` (Employee ID)
**Query Parameters**:
- `month`: Filter by month (YYYY-MM)
- `limit`: Number of records (default: 30)

**Response**:
```json
{
  "success": true,
  "data": {
    "emp_id": "EMP001",
    "name": "John Doe",
    "records": [
      {
        "date": "2024-01-15",
        "login_time": "09:00:00",
        "logout_time": "17:30:00",
        "total_hours": 8.5,
        "status": "present"
      }
    ],
    "summary": {
      "total_days": 20,
      "present_days": 18,
      "absent_days": 2,
      "total_hours": 153.0,
      "average_hours": 8.5
    }
  }
}
```

### GET /attendance/export
**Purpose**: Export attendance data to CSV (Admin only)
**Headers**: `Authorization: Bearer <token>`
**Query Parameters**:
- `date_from`: Start date (YYYY-MM-DD)
- `date_to`: End date (YYYY-MM-DD)
- `emp_id`: Filter by employee (optional)

**Response**: CSV file download

### GET /attendance/stats
**Purpose**: Get attendance statistics
**Headers**: `Authorization: Bearer <token>`
**Query Parameters**:
- `period`: `week`, `month`, `year` (default: month)

**Response**:
```json
{
  "success": true,
  "data": {
    "period": "month",
    "total_employees": 25,
    "present_today": 20,
    "absent_today": 5,
    "average_attendance_rate": 92.5,
    "daily_breakdown": [
      {
        "date": "2024-01-15",
        "present": 20,
        "absent": 5,
        "rate": 80.0
      }
    ],
    "department_breakdown": [
      {
        "department": "Engineering",
        "employees": 10,
        "attendance_rate": 95.0
      }
    ]
  }
}
```

## Face Recognition Endpoints

### POST /face/login
**Purpose**: Face recognition login
**Request**:
```json
{
  "face_image": "base64_encoded_image_string"
}
```
**Response**:
```json
{
  "success": true,
  "data": {
    "emp_id": "EMP001",
    "name": "John Doe",
    "role": "employee",
    "confidence": 0.95,
    "login_time": "2024-01-15T09:00:00Z"
  },
  "message": "Login successful"
}
```

### POST /face/logout
**Purpose**: Face recognition logout
**Request**:
```json
{
  "face_image": "base64_encoded_image_string"
}
```
**Response**:
```json
{
  "success": true,
  "data": {
    "emp_id": "EMP001",
    "name": "John Doe",
    "logout_time": "2024-01-15T17:30:00Z",
    "total_hours": 8.5
  },
  "message": "Logout successful"
}
```

### POST /face/register
**Purpose**: Register new face for employee
**Headers**: `Authorization: Bearer <token>`
**Request**:
```json
{
  "emp_id": "EMP001",
  "face_images": [
    "base64_encoded_image_string_1",
    "base64_encoded_image_string_2",
    "base64_encoded_image_string_3"
  ]
}
```
**Response**:
```json
{
  "success": true,
  "data": {
    "emp_id": "EMP001",
    "face_encoding_generated": true,
    "quality_score": 0.92
  },
  "message": "Face registered successfully"
}
```

### POST /face/verify
**Purpose**: Verify face without marking attendance
**Request**:
```json
{
  "face_image": "base64_encoded_image_string"
}
```
**Response**:
```json
{
  "success": true,
  "data": {
    "verified": true,
    "emp_id": "EMP001",
    "name": "John Doe",
    "confidence": 0.95
  }
}
```

## Error Response Format

### Standard Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {
      "field": "Specific error details"
    }
  },
  "timestamp": "2024-01-15T10:00:00Z"
}
```

### Common Error Codes
- `VALIDATION_ERROR`: Invalid input data
- `AUTHENTICATION_FAILED`: Face not recognized
- `AUTHORIZATION_DENIED`: Insufficient permissions
- `RESOURCE_NOT_FOUND`: Employee/record not found
- `DUPLICATE_RESOURCE`: Employee ID already exists
- `FACE_NOT_DETECTED`: No face found in image
- `LOW_QUALITY_IMAGE`: Image quality too low
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_SERVER_ERROR`: Server error

## HTTP Status Codes

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Duplicate resource
- `422 Unprocessable Entity`: Validation error
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## Rate Limiting

- **Face Recognition**: 10 requests per minute per IP
- **General API**: 100 requests per minute per user
- **Export**: 5 requests per hour per admin

## Security Headers

All responses include:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000` (HTTPS only)

## WebSocket Events (Future Enhancement)

### Connection Endpoint
`ws://localhost:8000/ws/attendance`

### Events
- `attendance_update`: Real-time attendance changes
- `employee_status`: Employee login/logout status
- `system_alerts`: System notifications

This API design ensures:
- **RESTful principles**: Proper HTTP methods and status codes
- **Security**: JWT authentication and authorization
- **Performance**: Pagination, filtering, and caching
- **Scalability**: Modular endpoint design
- **Maintainability**: Consistent response formats
- **Documentation**: Clear request/response examples
