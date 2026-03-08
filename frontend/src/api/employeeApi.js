import apiClient from './axiosClient'

export const employeeApi = {
  // Get all employees
  getEmployees: async (filters = {}) => {
    const params = new URLSearchParams()
    
    if (filters.search) params.append('search', filters.search)
    if (filters.role) params.append('role', filters.role)
    if (filters.department) params.append('department', filters.department)
    if (filters.is_active !== undefined) params.append('is_active', filters.is_active)
    if (filters.page) params.append('page', filters.page)
    if (filters.limit) params.append('limit', filters.limit)
    
    const response = await apiClient.get(`/api/v1/employees?${params}`)
    return response.data
  },

  // Get employee by ID
  getEmployee: async (empId) => {
    const response = await apiClient.get(`/api/v1/employees/${empId}`)
    return response.data
  },

  // Create new employee
  createEmployee: async (employeeData) => {
    const response = await apiClient.post('/api/v1/employees', employeeData)
    return response.data
  },

  // Update employee
  updateEmployee: async (empId, updateData) => {
    const response = await apiClient.put(`/api/v1/employees/${empId}`, updateData)
    return response.data
  },

  // Delete employee
  deleteEmployee: async (empId) => {
    const response = await apiClient.delete(`/api/v1/employees/${empId}`)
    return response.data
  },

  // Recapture face
  recaptureFace: async (empId, faceImage) => {
    const response = await apiClient.post(`/api/v1/employees/${empId}/recapture-face`, {
      face_image: faceImage
    })
    return response.data
  },

  // Get employee statistics
  getEmployeeStats: async () => {
    const response = await apiClient.get('/api/v1/employees/stats/summary')
    return response.data
  }
}
