# Architecture Flow Documentation

## Backend Architecture Flow

### Request Processing Pipeline
```
HTTP Request
    ↓
CORS & Security Middleware
    ↓
Authentication Middleware
    ↓
Router Layer (FastAPI)
    ↓
Dependency Injection
    ↓
Service Layer (Business Logic)
    ↓
Model Layer (Data Validation)
    ↓
Database Layer (MongoDB)
    ↓
Response Formatting
    ↓
HTTP Response
```

### Layer Responsibilities

#### 1. Router Layer (`/routers/`)
- **Purpose**: HTTP endpoint definitions
- **Responsibilities**:
  - Route definitions (`@app.get`, `@app.post`, etc.)
  - Request parameter validation
  - Response status codes
  - Dependency injection setup
- **Rules**: Only HTTP-related logic, no business logic

#### 2. Service Layer (`/services/`)
- **Purpose**: Business logic implementation
- **Responsibilities**:
  - Face recognition algorithms
  - Attendance calculations
  - Employee management logic
  - Data transformation
- **Rules**: No HTTP or database code, pure business logic

#### 3. Model Layer (`/models/`)
- **Purpose**: Data structure definitions
- **Responsibilities**:
  - MongoDB document schemas
  - Data validation rules
  - Database indexes
  - Relationship definitions

#### 4. Schema Layer (`/schemas/`)
- **Purpose**: API contract definitions
- **Responsibilities**:
  - Request/response validation
  - Data serialization/deserialization
  - API documentation models

## Frontend Architecture Flow

### Component Hierarchy
```
App.jsx
    ↓
Layout Components
    ├── Navbar.jsx
    ├── Sidebar.jsx
    └── Footer.jsx
    ↓
Page Components
    ├── DashboardPage.jsx
    ├── EmployeesPage.jsx
    ├── AttendancePage.jsx
    └── FaceLoginPage.jsx
    ↓
Feature Components
    ├── EmployeeTable.jsx
    ├── AttendanceTable.jsx
    ├── FaceCamera.jsx
    └── DashboardCards.jsx
    ↓
Common Components
    ├── Button.jsx
    ├── Input.jsx
    ├── Modal.jsx
    └── Loading.jsx
```

### State Management Flow
```
User Action
    ↓
Component Event Handler
    ↓
Custom Hook (useXXX)
    ↓
API Service Call
    ↓
Store Update (Zustand)
    ↓
Component Re-render
    ↓
UI Update
```

## Data Flow: Complete System

### Face Recognition Login Flow
```
1. Frontend: FaceLoginPage.jsx
   ├── Initialize camera (useCamera hook)
   ├── Start video stream
   └── Capture frame on user action

2. Frontend: useFaceRecognition hook
   ├── Process captured frame
   ├── Send to backend API
   └── Handle response

3. Backend: Face Router
   ├── POST /face/login
   ├── Validate request
   └── Call face service

4. Backend: Face Service
   ├── Receive image data
   ├── OpenCV face detection
   ├── Generate face encoding (128D vector)
   └── Compare with database

5. Backend: Database Layer
   ├── Query employee collection
   ├── Find matching face encoding
   └── Return employee data

6. Backend: Response
   ├── Generate JWT token
   ├── Return employee info
   └── Mark login time in attendance

7. Frontend: Store Update
   ├── Update auth store
   ├── Set user session
   └── Redirect to dashboard

8. Frontend: UI Update
   ├── Update navbar user info
   ├── Show welcome message
   └── Load dashboard data
```

### Attendance Recording Flow
```
1. Employee Face Login
   ├── Face recognition successful
   ├── Create attendance record
   └── Set login_time, date, emp_id

2. During Day
   ├── Employee works normally
   ├── System tracks active session
   └── Periodic status updates

3. Employee Face Logout
   ├── Face recognition verification
   ├── Update attendance record
   └── Set logout_time

4. Dashboard Update
   ├── Real-time data fetch
   ├── Update attendance charts
   └── Refresh statistics
```

### Employee Management Flow (Admin)
```
1. Admin: EmployeesPage.jsx
   ├── Load employee list
   ├── Display EmployeeTable
   └── Handle CRUD operations

2. Add Employee
   ├── Open modal with form
   ├── Capture face via FaceCamera
   ├── Send data to backend
   └── Update employee list

3. Backend Processing
   ├── Validate employee data
   ├── Generate face encoding
   ├── Store in MongoDB
   └── Return success response

4. Frontend Update
   ├── Refresh employee list
   ├── Show success message
   └── Update dashboard stats
```

## API Design Architecture

### RESTful API Structure
```
Base URL: http://localhost:8000/api/v1

Authentication
├── POST /auth/login
├── POST /auth/logout
└── POST /auth/refresh

Employees
├── GET /employees
├── POST /employees
├── GET /employees/{id}
├── PUT /employees/{id}
├── DELETE /employees/{id}
└── POST /employees/{id}/recapture-face

Attendance
├── GET /attendance
├── GET /attendance/today
├── GET /attendance/date/{date}
├── GET /attendance/employee/{id}
├── GET /attendance/export
└── GET /attendance/stats

Face Recognition
├── POST /face/login
├── POST /face/logout
├── POST /face/register
└── POST /face/verify
```

### Request/Response Patterns
```
Standard Response Format:
{
  "success": true,
  "data": {},
  "message": "Operation successful",
  "timestamp": "2024-01-01T00:00:00Z"
}

Error Response Format:
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {}
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Security Architecture

### Authentication Flow
```
1. User Login (Face Recognition)
   ├── Face verification
   ├── Generate JWT token
   └── Return token to client

2. Token Storage
   ├── Store in HTTP-only cookie
   ├── Or secure local storage
   └── Set expiration time

3. API Requests
   ├── Include JWT in Authorization header
   ├── Backend middleware validation
   └── Token refresh on expiry
```

### Authorization Levels
```
Admin Role:
├── Full employee management
├── Attendance record access
├── System configuration
└── Export capabilities

Employee Role:
├── Face login/logout
├── Personal attendance view
├── Profile management
└── Limited dashboard access
```

## Performance Architecture

### Caching Strategy
```
Frontend Caching:
├── React Query for API calls
├── Local storage for user data
└── Component state memoization

Backend Caching:
├── Redis for session storage
├── Face encoding cache
└── Database query caching
```

### Database Optimization
```
MongoDB Indexes:
├── employees.emp_id (unique)
├── attendance.emp_id + date (compound)
├── attendance.date (for date range queries)
└── employees.face_encoding (for similarity search)
```

## Scalability Architecture

### Horizontal Scaling
```
Backend:
├── Load balancer
├── Multiple FastAPI instances
├── MongoDB replica set
└── Redis cluster

Frontend:
├── CDN for static assets
├── Progressive Web App
└── Service workers
```

### Microservices Preparation
```
Service Separation:
├── Authentication Service
├── Employee Management Service
├── Attendance Service
├── Face Recognition Service
└── Notification Service
```

This architecture ensures:
- **Maintainability**: Clear separation of concerns
- **Scalability**: Modular design for easy scaling
- **Testability**: Each layer can be tested independently
- **Security**: Proper authentication and authorization
- **Performance**: Optimized data flow and caching
