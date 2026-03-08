import apiClient from './axiosClient'

export const authApi = {
  // Refresh token
  refreshToken: async (refreshToken) => {
    const response = await apiClient.post('/api/v1/auth/refresh', {
      refresh_token: refreshToken
    })
    return response.data
  },

  // Get current user info
  getCurrentUser: async () => {
    const response = await apiClient.get('/api/v1/auth/me')
    return response.data
  },

  // Logout
  logout: async () => {
    const response = await apiClient.post('/api/v1/auth/logout')
    return response.data
  },

  // Validate token
  validateToken: async () => {
    const response = await apiClient.get('/api/v1/auth/validate')
    return response.data
  },

  // Change user role (admin only)
  changeRole: async (empId, newRole) => {
    const response = await apiClient.post(`/api/v1/auth/change-role/${empId}`, {
      new_role: newRole
    })
    return response.data
  },

  // Get user permissions
  getPermissions: async () => {
    const response = await apiClient.get('/api/v1/auth/permissions')
    return response.data
  },

  // Get session info
  getSessionInfo: async () => {
    const response = await apiClient.get('/api/v1/auth/session-info')
    return response.data
  }
}
