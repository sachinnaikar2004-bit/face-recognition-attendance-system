import React, { useState } from 'react'
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom'
import { 
  Home, 
  Calendar, 
  User, 
  LogOut, 
  Menu,
  X,
  Clock
} from 'lucide-react'
import { useAuth } from '../hooks/useAuth'

export const EmployeeLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const location = useLocation()
  const navigate = useNavigate()
  const { user, logout, isUserLoggedIn, getUserLoginTime, getUserWorkDuration } = useAuth()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  const menuItems = [
    {
      title: 'Dashboard',
      icon: Home,
      path: '/employee/dashboard',
      active: location.pathname === '/employee/dashboard'
    },
    {
      title: 'My Attendance',
      icon: Calendar,
      path: '/employee/attendance',
      active: location.pathname.startsWith('/employee/attendance')
    },
    {
      title: 'Profile',
      icon: User,
      path: '/employee/profile',
      active: location.pathname.startsWith('/employee/profile')
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <div className={`sidebar ${sidebarOpen ? '' : 'sidebar-closed'} lg:translate-x-0`}>
        <div className="flex h-16 items-center justify-between px-6 border-b border-gray-200">
          <h1 className="text-xl font-semibold text-gray-900">
            Employee Portal
          </h1>
          <button
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden p-1 rounded-md hover:bg-gray-100"
          >
            <X className="h-5 w-5" />
          </button>
        </div>
        
        <nav className="flex-1 px-4 py-6">
          <ul className="space-y-2">
            {menuItems.map((item) => (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    item.active
                      ? 'bg-primary-100 text-primary-700'
                      : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                  }`}
                >
                  <item.icon className="h-5 w-5 mr-3" />
                  {item.title}
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        {/* User Info */}
        <div className="border-t border-gray-200 p-4">
          <div className="mb-4 p-3 bg-primary-50 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-primary-900">Today's Status</span>
              <span className={`badge ${isUserLoggedIn() ? 'badge-success' : 'badge-gray'}`}>
                {isUserLoggedIn() ? 'Active' : 'Inactive'}
              </span>
            </div>
            {isUserLoggedIn() && (
              <div className="space-y-1">
                <div className="flex items-center text-xs text-primary-700">
                  <Clock className="h-3 w-3 mr-1" />
                  Login: {getUserLoginTime()}
                </div>
                <div className="flex items-center text-xs text-primary-700">
                  <Clock className="h-3 w-3 mr-1" />
                  Duration: {getUserWorkDuration()}
                </div>
              </div>
            )}
          </div>
          
          <div className="flex items-center px-3 py-2">
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">{user?.name}</p>
              <p className="text-xs text-gray-500">{user?.emp_id}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Top Navigation */}
        <header className="navbar">
          <div className="flex h-16 items-center justify-between px-6">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden p-2 rounded-md hover:bg-gray-100"
            >
              <Menu className="h-5 w-5" />
            </button>

            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">
                Employee Portal
              </span>
              <button
                onClick={handleLogout}
                className="flex items-center px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
              >
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </button>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-auto">
          <div className="p-6">
            <Outlet />
          </div>
        </main>
      </div>

      {/* Mobile Sidebar Overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  )
}
