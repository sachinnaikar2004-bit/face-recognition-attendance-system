import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Link, useLocation } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Users, 
  Calendar, 
  Camera, 
  Settings, 
  Menu, 
  X,
  LogOut,
  Bell,
  Search
} from 'lucide-react'
import { useAuthStore } from '../../store/authStore'

const sidebarItems = [
  { icon: LayoutDashboard, label: 'Dashboard', path: '/admin/dashboard' },
  { icon: Users, label: 'Employees', path: '/admin/employees' },
  { icon: Calendar, label: 'Attendance', path: '/admin/attendance' },
  { icon: Camera, label: 'Face Login', path: '/face-login' },
  { icon: Settings, label: 'Settings', path: '/admin/settings' },
]

export const Sidebar = ({ isCollapsed, setIsCollapsed, isMobile }) => {
  const location = useLocation()
  const { user, logout } = useAuthStore()

  const handleLogout = () => {
    logout()
  }

  return (
    <>
      {/* Mobile overlay */}
      <AnimatePresence>
        {isMobile && !isCollapsed && (
          <motion.div
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setIsCollapsed(true)}
          />
        )}
      </AnimatePresence>

      <motion.aside
        className={`fixed left-0 top-0 h-full bg-white border-r border-gray-200 z-50 ${
          isCollapsed ? 'w-20' : 'w-64'
        } transition-all duration-300 ease-in-out`}
        initial={false}
        animate={{ width: isCollapsed ? 80 : 256 }}
      >
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-gray-100">
            {!isCollapsed && (
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex items-center space-x-3"
              >
                <div className="w-10 h-10 bg-gradient-primary rounded-xl flex items-center justify-center">
                  <Camera className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-lg font-bold text-gray-900">FaceAttend</h1>
                  <p className="text-xs text-gray-500">Smart Attendance</p>
                </div>
              </motion.div>
            )}
            
            <button
              onClick={() => setIsCollapsed(!isCollapsed)}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              {isCollapsed ? <Menu className="w-5 h-5" /> : <X className="w-5 h-5" />}
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-2">
            {sidebarItems.map((item) => {
              const isActive = location.pathname === item.path
              return (
                <Link key={item.path} to={item.path} onClick={() => isMobile && setIsCollapsed(true)}>
                  <motion.div
                    className={`flex items-center space-x-3 px-3 py-2.5 rounded-xl transition-all duration-200 ${
                      isActive
                        ? 'bg-primary/10 text-primary font-medium'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <item.icon className="w-5 h-5 flex-shrink-0" />
                    {!isCollapsed && (
                      <motion.span
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="text-sm"
                      >
                        {item.label}
                      </motion.span>
                    )}
                  </motion.div>
                </Link>
              )
            })}
          </nav>

          {/* User Section */}
          <div className="p-4 border-t border-gray-100">
            {!isCollapsed && user && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-3"
              >
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                    <span className="text-sm font-medium text-primary">
                      {user.name?.split(' ').map(n => n[0]).join('') || 'U'}
                    </span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {user.name || 'User'}
                    </p>
                    <p className="text-xs text-gray-500 truncate">
                      {user.role || 'Admin'}
                    </p>
                  </div>
                </div>
                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-2 w-full px-3 py-2 text-sm text-gray-600 hover:bg-red-50 hover:text-red-600 rounded-xl transition-all duration-200"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Logout</span>
                </button>
              </motion.div>
            )}
            
            {isCollapsed && (
              <button
                onClick={handleLogout}
                className="w-full p-2 text-gray-600 hover:bg-red-50 hover:text-red-600 rounded-xl transition-all duration-200 flex justify-center"
              >
                <LogOut className="w-5 h-5" />
              </button>
            )}
          </div>
        </div>
      </motion.aside>
    </>
  )
}
