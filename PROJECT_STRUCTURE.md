# AI Face Recognition Attendance System - Project Structure

## Overview
A production-ready face recognition attendance system with React frontend and FastAPI backend, following clean architecture principles.

## Complete Folder Structure

```
face_attendance/
├── README.md
├── docker-compose.yml
├── .env.example
├── .gitignore
│
├── backend/
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env
│   ├── alembic.ini
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       │
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   ├── security.py
│       │   └── exceptions.py
│       │
│       ├── database/
│       │   ├── __init__.py
│       │   ├── mongodb.py
│       │   └── connection.py
│       │
│       ├── models/
│       │   ├── __init__.py
│       │   ├── employee_model.py
│       │   ├── attendance_model.py
│       │   └── base_model.py
│       │
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── employee_schema.py
│       │   ├── attendance_schema.py
│       │   ├── auth_schema.py
│       │   └── response_schema.py
│       │
│       ├── routers/
│       │   ├── __init__.py
│       │   ├── employee_router.py
│       │   ├── attendance_router.py
│       │   ├── face_router.py
│       │   └── auth_router.py
│       │
│       ├── services/
│       │   ├── __init__.py
│       │   ├── face_service.py
│       │   ├── attendance_service.py
│       │   ├── employee_service.py
│       │   └── auth_service.py
│       │
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── face_encoding.py
│       │   ├── camera_capture.py
│       │   ├── csv_export.py
│       │   └── image_processing.py
│       │
│       ├── dependencies/
│       │   ├── __init__.py
│       │   ├── auth_dependency.py
│       │   └── database_dependency.py
│       │
│       └── middleware/
│           ├── __init__.py
│           ├── cors_middleware.py
│           └── logging_middleware.py
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── Dockerfile
│   ├── .env
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       │
│       ├── api/
│       │   ├── axiosClient.js
│       │   ├── employeeApi.js
│       │   ├── attendanceApi.js
│       │   ├── faceApi.js
│       │   └── authApi.js
│       │
│       ├── pages/
│       │   ├── LoginPage.jsx
│       │   ├── DashboardPage.jsx
│       │   ├── EmployeesPage.jsx
│       │   ├── AttendancePage.jsx
│       │   └── FaceLoginPage.jsx
│       │
│       ├── components/
│       │   ├── common/
│       │   │   ├── Button.jsx
│       │   │   ├── Input.jsx
│       │   │   ├── Modal.jsx
│       │   │   ├── Loading.jsx
│       │   │   └── Toast.jsx
│       │   ├── layout/
│       │   │   ├── Navbar.jsx
│       │   │   ├── Sidebar.jsx
│       │   │   └── Footer.jsx
│       │   ├── features/
│       │   │   ├── EmployeeTable.jsx
│       │   │   ├── AttendanceTable.jsx
│       │   │   ├── FaceCamera.jsx
│       │   │   └── DashboardCards.jsx
│       │   └── charts/
│       │       ├── LineChart.jsx
│       │       ├── BarChart.jsx
│       │       └── PieChart.jsx
│       │
│       ├── hooks/
│       │   ├── useCamera.js
│       │   ├── useFaceRecognition.js
│       │   ├── useAuth.js
│       │   └── useAttendance.js
│       │
│       ├── store/
│       │   ├── authStore.js
│       │   ├── employeeStore.js
│       │   └── attendanceStore.js
│       │
│       ├── layouts/
│       │   ├── AdminLayout.jsx
│       │   ├── EmployeeLayout.jsx
│       │   └── PublicLayout.jsx
│       │
│       ├── styles/
│       │   ├── global.css
│       │   ├── components.css
│       │   └── utilities.css
│       │
│       ├── utils/
│       │   ├── constants.js
│       │   ├── helpers.js
│       │   └── validators.js
│       │
│       └── assets/
│           ├── images/
│           ├── icons/
│           └── fonts/
│
├── docs/
│   ├── api_documentation.md
│   ├── deployment_guide.md
│   └── user_manual.md
│
├── scripts/
│   ├── setup.sh
│   ├── backup_database.sh
│   └── deploy.sh
│
└── tests/
    ├── backend/
    │   ├── test_employee_service.py
    │   ├── test_attendance_service.py
    │   ├── test_face_service.py
    │   └── conftest.py
    │
    └── frontend/
        ├── components/
        ├── hooks/
        └── utils/
```

## Folder Explanations

### Backend Structure

#### `/backend/app/core/`
- **config.py**: Application configuration, environment variables
- **security.py**: JWT authentication, password hashing
- **exceptions.py**: Custom exception handlers

#### `/backend/app/database/`
- **mongodb.py**: MongoDB connection setup and utilities
- **connection.py**: Database connection management

#### `/backend/app/models/`
- **employee_model.py**: Employee data model
- **attendance_model.py**: Attendance record model
- **base_model.py**: Base MongoDB model with common fields

#### `/backend/app/schemas/`
- **employee_schema.py**: Pydantic schemas for employee data validation
- **attendance_schema.py**: Pydantic schemas for attendance data
- **auth_schema.py**: Authentication request/response schemas
- **response_schema.py**: Common API response schemas

#### `/backend/app/routers/`
- **employee_router.py**: Employee management endpoints
- **attendance_router.py**: Attendance record endpoints
- **face_router.py**: Face recognition endpoints
- **auth_router.py**: Authentication endpoints

#### `/backend/app/services/`
- **employee_service.py**: Employee business logic
- **attendance_service.py**: Attendance business logic
- **face_service.py**: Face recognition business logic
- **auth_service.py**: Authentication business logic

#### `/backend/app/utils/`
- **face_encoding.py**: Face encoding generation and comparison
- **camera_capture.py**: Camera utilities for face capture
- **csv_export.py**: CSV export functionality
- **image_processing.py**: Image processing utilities

#### `/backend/app/dependencies/`
- **auth_dependency.py**: JWT authentication dependency
- **database_dependency.py**: Database connection dependency

#### `/backend/app/middleware/`
- **cors_middleware.py**: CORS configuration
- **logging_middleware.py**: Request logging middleware

### Frontend Structure

#### `/frontend/src/api/`
- **axiosClient.js**: Axios configuration with interceptors
- **employeeApi.js**: Employee-related API calls
- **attendanceApi.js**: Attendance-related API calls
- **faceApi.js**: Face recognition API calls
- **authApi.js**: Authentication API calls

#### `/frontend/src/pages/`
- **LoginPage.jsx**: Login page
- **DashboardPage.jsx**: Admin dashboard
- **EmployeesPage.jsx**: Employee management
- **AttendancePage.jsx**: Attendance records
- **FaceLoginPage.jsx**: Face recognition login

#### `/frontend/src/components/`
- **common/**: Reusable UI components
- **layout/**: Layout components (Navbar, Sidebar, Footer)
- **features/**: Feature-specific components
- **charts/**: Chart components using Recharts

#### `/frontend/src/hooks/`
- **useCamera.js**: Camera management hook
- **useFaceRecognition.js**: Face recognition logic
- **useAuth.js**: Authentication state management
- **useAttendance.js**: Attendance data management

#### `/frontend/src/store/`
- **authStore.js**: Authentication state (Zustand)
- **employeeStore.js**: Employee data state
- **attendanceStore.js**: Attendance data state

#### `/frontend/src/layouts/**
- **AdminLayout.jsx**: Admin panel layout
- **EmployeeLayout.jsx**: Employee panel layout
- **PublicLayout.jsx**: Public pages layout

#### `/frontend/src/styles/`
- **global.css**: Global styles and Tailwind imports
- **components.css**: Component-specific styles
- **utilities.css**: Custom utility classes

## Architecture Flow

### Backend Architecture Flow
```
Request → Router → Service → Model → MongoDB → Response
    ↓         ↓         ↓       ↓        ↓
  Auth    Business  Data    Database  Validation
Validation  Logic   Models  Operations
```

### Frontend Architecture Flow
```
User Action → Component → Hook → API Service → Store → UI Update
     ↓           ↓        ↓        ↓         ↓
   Event      UI      Business  HTTP      State
  Handler   Render   Logic    Request  Management
```

## Clean Architecture Principles

1. **Separation of Concerns**: Each layer has specific responsibilities
2. **Dependency Inversion**: High-level modules don't depend on low-level modules
3. **Single Responsibility**: Each class/module has one reason to change
4. **Open/Closed Principle**: Open for extension, closed for modification
5. **Interface Segregation**: Clients shouldn't depend on unused interfaces

## Data Flow: Camera → Backend → MongoDB → Dashboard

```
1. Camera Capture (Frontend)
   ├── Video stream from webcam
   ├── Frame extraction
   └── Face detection

2. Face Recognition (Backend)
   ├── Receive image data
   ├── OpenCV face detection
   ├── Generate 128D encoding
   └── Compare with database

3. Database Operations (MongoDB)
   ├── Query employee face encodings
   ├── Insert attendance record
   └── Update employee status

4. Dashboard Update (Frontend)
   ├── Real-time data fetching
   ├── Chart visualization
   └── UI state management
```

## Next Steps

1. Set up the folder structure
2. Configure development environment
3. Implement core models and schemas
4. Build API endpoints
5. Create frontend components
6. Integrate face recognition system
7. Add authentication and authorization
8. Implement real-time features
9. Add testing and documentation
10. Deploy to production
