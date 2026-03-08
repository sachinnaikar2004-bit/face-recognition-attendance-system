import React from 'react'
import { motion } from 'framer-motion'
import { 
  Users, 
  UserCheck, 
  UserX, 
  Clock, 
  TrendingUp, 
  Calendar,
  Activity,
  ArrowUpRight,
  ArrowDownRight
} from 'lucide-react'
import { useAuthStore } from '../store/authStore'
import { StatCard } from '../components/ui/Card'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

export const DashboardPage = () => {
  const { user } = useAuthStore()

  // Sample data for charts
  const attendanceTrendData = [
    { day: 'Mon', present: 45, absent: 5 },
    { day: 'Tue', present: 48, absent: 2 },
    { day: 'Wed', present: 46, absent: 4 },
    { day: 'Thu', present: 49, absent: 1 },
    { day: 'Fri', present: 47, absent: 3 },
    { day: 'Sat', present: 35, absent: 15 },
    { day: 'Sun', present: 20, absent: 30 },
  ]

  const monthlyAttendanceData = [
    { month: 'Jan', attendance: 92 },
    { month: 'Feb', attendance: 88 },
    { month: 'Mar', attendance: 95 },
    { month: 'Apr', attendance: 90 },
    { month: 'May', attendance: 93 },
    { month: 'Jun', attendance: 89 },
  ]

  const departmentData = [
    { name: 'Engineering', value: 35, color: '#2563EB' },
    { name: 'Sales', value: 25, color: '#22C55E' },
    { name: 'HR', value: 20, color: '#F59E0B' },
    { name: 'Marketing', value: 20, color: '#8B5CF6' },
  ]

  const recentActivities = [
    { 
      id: 1, 
      employee: 'John Doe', 
      action: 'Checked In', 
      time: '9:15 AM', 
      status: 'on-time',
      avatar: 'JD'
    },
    { 
      id: 2, 
      employee: 'Jane Smith', 
      action: 'Checked In', 
      time: '9:30 AM', 
      status: 'late',
      avatar: 'JS'
    },
    { 
      id: 3, 
      employee: 'Mike Johnson', 
      action: 'Checked Out', 
      time: '5:45 PM', 
      status: 'completed',
      avatar: 'MJ'
    },
    { 
      id: 4, 
      employee: 'Sarah Williams', 
      action: 'Checked In', 
      time: '8:45 AM', 
      status: 'on-time',
      avatar: 'SW'
    },
  ]

  const stats = [
    {
      title: 'Total Employees',
      value: '248',
      change: '+12',
      changeType: 'increase',
      icon: Users,
      color: 'primary'
    },
    {
      title: 'Present Today',
      value: '186',
      change: '+8',
      changeType: 'increase',
      icon: UserCheck,
      color: 'success'
    },
    {
      title: 'Absent Today',
      value: '62',
      change: '-8',
      changeType: 'decrease',
      icon: UserX,
      color: 'danger'
    },
    {
      title: 'Late Arrivals',
      value: '24',
      change: '+2',
      changeType: 'neutral',
      icon: Clock,
      color: 'warning'
    },
  ]

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="bg-gradient-primary rounded-2xl p-8 text-white">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold mb-2">
                Welcome back, {user?.name || 'User'}! 👋
              </h1>
              <p className="text-white/90 text-lg">
                Here's what's happening with your attendance system today.
              </p>
            </div>
            <div className="hidden lg:block">
              <div className="bg-white/20 backdrop-blur-sm rounded-xl p-6">
                <div className="text-center">
                  <p className="text-3xl font-bold">75%</p>
                  <p className="text-white/80">Today's Attendance</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Stats Grid */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
      >
        {stats.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 + index * 0.1 }}
          >
            <StatCard {...stat} />
          </motion.div>
        ))}
      </motion.div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Attendance Trend Chart */}
        <motion.div
          className="bg-white rounded-xl shadow-sm border border-gray-100 p-6"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Weekly Attendance Trend</h3>
            <div className="flex items-center space-x-2 text-sm">
              <div className="flex items-center space-x-1">
                <div className="w-3 h-3 bg-green-500 rounded-full" />
                <span className="text-gray-600">Present</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-3 h-3 bg-red-500 rounded-full" />
                <span className="text-gray-600">Absent</span>
              </div>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={attendanceTrendData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="day" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'white', 
                  border: '1px solid #e5e7eb', 
                  borderRadius: '8px' 
                }}
              />
              <Line 
                type="monotone" 
                dataKey="present" 
                stroke="#22C55E" 
                strokeWidth={2}
                dot={{ fill: '#22C55E', r: 4 }}
              />
              <Line 
                type="monotone" 
                dataKey="absent" 
                stroke="#EF4444" 
                strokeWidth={2}
                dot={{ fill: '#EF4444', r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Department Distribution */}
        <motion.div
          className="bg-white rounded-xl shadow-sm border border-gray-100 p-6"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Department Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={departmentData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={5}
                dataKey="value"
              >
                {departmentData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'white', 
                  border: '1px solid #e5e7eb', 
                  borderRadius: '8px' 
                }}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="grid grid-cols-2 gap-4 mt-4">
            {departmentData.map((dept) => (
              <div key={dept.name} className="flex items-center space-x-2">
                <div 
                  className="w-3 h-3 rounded-full" 
                  style={{ backgroundColor: dept.color }}
                />
                <span className="text-sm text-gray-600">{dept.name}</span>
                <span className="text-sm font-medium text-gray-900">{dept.value}%</span>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Monthly Attendance & Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Monthly Attendance Bar Chart */}
        <motion.div
          className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-100 p-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5 }}
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Monthly Attendance Rate</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={monthlyAttendanceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="month" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'white', 
                  border: '1px solid #e5e7eb', 
                  borderRadius: '8px' 
                }}
              />
              <Bar 
                dataKey="attendance" 
                fill="#2563EB" 
                radius={[8, 8, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Recent Activity */}
        <motion.div
          className="bg-white rounded-xl shadow-sm border border-gray-100 p-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Recent Activity</h3>
          <div className="space-y-4">
            {recentActivities.map((activity, index) => (
              <motion.div
                key={activity.id}
                className="flex items-center space-x-3"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: 0.7 + index * 0.1 }}
              >
                <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                  <span className="text-xs font-medium text-primary">
                    {activity.avatar}
                  </span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {activity.employee}
                  </p>
                  <p className="text-xs text-gray-500">
                    {activity.action} • {activity.time}
                  </p>
                </div>
                <div className={`w-2 h-2 rounded-full ${
                  activity.status === 'on-time' ? 'bg-green-500' :
                  activity.status === 'late' ? 'bg-yellow-500' : 'bg-blue-500'
                }`} />
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  )
}
