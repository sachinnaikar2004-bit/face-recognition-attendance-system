# AI Face Recognition Attendance System

A production-ready face recognition attendance system built with React frontend and FastAPI backend, following clean architecture principles.

## 🚀 Features

### Admin Panel
- **Dashboard** with real-time analytics and charts
- **Employee Management** (Add, Delete, Update, Recapture face)
- **Attendance Records** with advanced filtering
- **CSV Export** functionality for reports
- **Search and Pagination** capabilities

### Employee Panel
- **Face Recognition Login** with high accuracy
- **Automatic Logout** detection
- **Personal Attendance History**
- **Profile Management**

### Face Recognition System
- **Real-time Face Detection** using OpenCV
- **128D Face Encoding** with dlib
- **High Accuracy Matching** algorithm
- **Quality Validation** for captured images
- **Multi-angle Face Registration**

## 🛠 Tech Stack

### Frontend
- **React 18** with Vite for fast development
- **React Router** for navigation
- **Axios** for HTTP requests
- **TailwindCSS** for modern styling
- **Zustand** for state management
- **Recharts** for analytics charts
- **OpenCV.js** for client-side face detection

### Backend
- **FastAPI** for high-performance API
- **MongoDB Atlas** for cloud database
- **Motor** for async MongoDB operations
- **OpenCV** for face detection
- **face_recognition** (dlib) for encoding
- **Pydantic** for data validation
- **JWT** for authentication

## 📁 Project Structure

```
face_attendance/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── core/          # Configuration & security
│   │   ├── database/      # MongoDB connection
│   │   ├── models/        # Data models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── routers/       # API endpoints
│   │   ├── services/      # Business logic
│   │   ├── utils/         # Utilities
│   │   └── dependencies/  # Dependencies
│   └── tests/             # Backend tests
├── frontend/               # React frontend
│   ├── src/
│   │   ├── api/          # API services
│   │   ├── pages/        # Page components
│   │   ├── components/   # Reusable components
│   │   ├── hooks/        # Custom hooks
│   │   ├── store/        # State management
│   │   ├── layouts/      # Layout components
│   │   └── styles/       # CSS styles
│   └── tests/            # Frontend tests
├── docs/                 # Documentation
└── scripts/              # Utility scripts
```

## 🏗 Architecture

### Clean Architecture Principles
- **Separation of Concerns**: Each layer has specific responsibilities
- **Dependency Inversion**: High-level modules don't depend on low-level modules
- **Single Responsibility**: Each class has one reason to change
- **Testability**: Each layer can be tested independently

### Data Flow
```
Camera Capture → Face Detection → Encoding → Database Comparison → Attendance Recording
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- MongoDB Atlas account
- Git

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd face_attendance
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd frontend
npm install
```

4. **Environment Configuration**
```bash
# Backend .env
MONGODB_URL=mongodb+srv://...
JWT_SECRET=your-secret-key
CORS_ORIGINS=http://localhost:5173

# Frontend .env
VITE_API_URL=http://localhost:8000
```

5. **Run the Application**
```bash
# Backend (Terminal 1)
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (Terminal 2)
cd frontend
npm run dev
```

6. **Access the Application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📊 Database Design

### Collections

#### Employees
```javascript
{
  _id: ObjectId,
  emp_id: "EMP001",
  name: "John Doe",
  email: "john@example.com",
  role: "employee",
  department: "Engineering",
  face_encoding: [0.1, 0.2, ..., 0.128],
  created_at: ISODate,
  updated_at: ISODate
}
```

#### Attendance
```javascript
{
  _id: ObjectId,
  emp_id: "EMP001",
  date: "2024-01-15",
  login_time: "09:00:00",
  logout_time: "17:30:00",
  total_hours: 8.5,
  status: "present",
  created_at: ISODate
}
```

## 🔐 Security Features

- **JWT Authentication** with refresh tokens
- **Role-based Access Control** (Admin/Employee)
- **Face Recognition** for secure login
- **CORS Protection** for API security
- **Input Validation** with Pydantic schemas
- **Rate Limiting** for API endpoints

## 📈 Performance Features

- **Async Database Operations** with Motor
- **Image Optimization** for fast processing
- **Caching Strategy** with Redis
- **Lazy Loading** for large datasets
- **Pagination** for API responses
- **Code Splitting** in React

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/v1/auth/login` - Face recognition login
- `POST /api/v1/auth/logout` - User logout
- `POST /api/v1/auth/refresh` - Refresh token

### Employee Endpoints
- `GET /api/v1/employees` - List all employees
- `POST /api/v1/employees` - Add new employee
- `PUT /api/v1/employees/{id}` - Update employee
- `DELETE /api/v1/employees/{id}` - Delete employee

### Attendance Endpoints
- `GET /api/v1/attendance` - Get attendance records
- `GET /api/v1/attendance/today` - Today's attendance
- `GET /api/v1/attendance/export` - Export to CSV

### Face Recognition Endpoints
- `POST /api/v1/face/login` - Face login
- `POST /api/v1/face/logout` - Face logout
- `POST /api/v1/face/register` - Register face

## 🎨 UI Design

### Theme
- **Primary Color**: #2563EB (Blue)
- **Background**: #F9FAFB (Light Gray)
- **Card Background**: White with shadow
- **Border Radius**: 8px
- **Animations**: Smooth transitions

### Design Inspiration
- Stripe Dashboard
- Vercel UI
- Notion clean design

## 🚀 Deployment

### Docker Deployment
```bash
docker-compose up -d
```

### Environment Variables
```bash
# Production
NODE_ENV=production
MONGODB_URL=mongodb+srv://...
JWT_SECRET=strong-secret-key
CORS_ORIGINS=https://yourdomain.com
```

## 📝 Development Guidelines

### Code Standards
- **ESLint** and **Prettier** for frontend
- **Black** and **Flake8** for backend
- **TypeScript** for type safety
- **Git Hooks** for pre-commit checks

### Contribution Guidelines
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 🐛 Troubleshooting

### Common Issues

#### Face Recognition Not Working
- Check camera permissions
- Ensure proper lighting
- Verify OpenCV installation
- Check face encoding quality

#### Database Connection Issues
- Verify MongoDB URL
- Check network connectivity
- Ensure proper credentials
- Check firewall settings

#### Frontend Build Issues
- Clear node_modules and reinstall
- Check Node.js version compatibility
- Verify environment variables
- Check for dependency conflicts

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

For support and questions:
- Create an issue in the repository
- Check the [documentation](docs/)
- Review the [FAQ](docs/faq.md)

## 🗺 Roadmap

### Version 2.0 Features
- [ ] Mobile app support
- [ ] Advanced analytics dashboard
- [ ] Multi-location support
- [ ] Biometric backup options
- [ ] Integration with HR systems

### Version 1.5 Features
- [ ] Real-time notifications
- [ ] Advanced reporting
- [ ] Bulk operations
- [ ] API rate limiting
- [ ] Performance monitoring

---

**Built with ❤️ using modern web technologies**
