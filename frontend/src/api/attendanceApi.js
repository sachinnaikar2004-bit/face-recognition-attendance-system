import apiClient from './axiosClient'

export const attendanceApi = {
  // Get attendance records
  getAttendance: async (filters = {}) => {
    const params = new URLSearchParams()
    
    if (filters.emp_id) params.append('emp_id', filters.emp_id)
    if (filters.date_from) params.append('date_from', filters.date_from)
    if (filters.date_to) params.append('date_to', filters.date_to)
    if (filters.status) params.append('status', filters.status)
    if (filters.page) params.append('page', filters.page)
    if (filters.limit) params.append('limit', filters.limit)
    
    const response = await apiClient.get(`/api/v1/attendance?${params}`)
    return response.data
  },

  // Get today's attendance
  getTodayAttendance: async () => {
    const response = await apiClient.get('/api/v1/attendance/today')
    return response.data
  },

  // Get attendance by date
  getAttendanceByDate: async (date) => {
    const response = await apiClient.get(`/api/v1/attendance/date/${date}`)
    return response.data
  },

  // Get employee attendance history
  getEmployeeAttendanceHistory: async (empId, days = 30) => {
    const response = await apiClient.get(`/api/v1/attendance/employee/${empId}?days=${days}`)
    return response.data
  },

  // Get attendance statistics
  getAttendanceStats: async (period = 'month') => {
    const response = await apiClient.get(`/api/v1/attendance/stats/summary?period=${period}`)
    return response.data
  },

  // Export attendance to CSV
  exportAttendance: async (filters = {}) => {
    const params = new URLSearchParams()
    
    if (filters.date_from) params.append('date_from', filters.date_from)
    if (filters.date_to) params.append('date_to', filters.date_to)
    if (filters.emp_id) params.append('emp_id', filters.emp_id)
    
    const response = await apiClient.get(`/api/v1/attendance/export?${params}`, {
      responseType: 'blob'
    })
    
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `attendance_export_${new Date().toISOString().split('T')[0]}.csv`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    
    return response.data
  },

  // Mark attendance (login/logout)
  markAttendance: async (attendanceType) => {
    const response = await apiClient.post(`/api/v1/attendance/mark/${attendanceType}`)
    return response.data
  }
}
