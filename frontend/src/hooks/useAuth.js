import { useCallback } from 'react'
import { useAuthStore } from '../store/authStore'
import { faceApi } from '../api/faceApi'

export const useAuth = () => {
  const {
    user,
    isAuthenticated,
    isLoading,
    permissions,
    login,
    logout,
    refreshToken,
    checkAuth,
    loadPermissions,
    updateUser,
    clearError
  } = useAuthStore()

  // Face login
  const faceLogin = useCallback(async (imageData) => {
    try {
      const result = await faceApi.login(imageData)
      const loginResult = await login(result)
      return loginResult
    } catch (error) {
      throw error
    }
  }, [login])

  // Face logout
  const faceLogout = useCallback(async (imageData) => {
    try {
      await faceApi.logout(imageData)
      await logout()
      return true
    } catch (error) {
      throw error
    }
  }, [logout])

  // Check if user has specific permission
  const hasPermission = useCallback((permission) => {
    return permissions.includes(permission)
  }, [permissions])

  // Check if user has any of the specified permissions
  const hasAnyPermission = useCallback((permissionList) => {
    return permissionList.some(permission => permissions.includes(permission))
  }, [permissions])

  // Check if user is admin
  const isAdmin = useCallback(() => {
    return user?.role === 'admin'
  }, [user])

  // Check if user is employee
  const isEmployee = useCallback(() => {
    return user?.role === 'employee'
  }, [user])

  // Get user dashboard route
  const getDashboardRoute = useCallback(() => {
    if (isAdmin()) {
      return '/admin/dashboard'
    } else if (isEmployee()) {
      return '/employee/dashboard'
    }
    return '/login'
  }, [isAdmin, isEmployee])

  // Initialize authentication on app load
  const initializeAuth = useCallback(async () => {
    const isValid = await checkAuth()
    if (isValid) {
      await loadPermissions()
    }
    return isValid
  }, [checkAuth, loadPermissions])

  return {
    // State
    user,
    isAuthenticated,
    isLoading,
    permissions,

    // Computed
    isAdmin,
    isEmployee,
    hasPermission,
    hasAnyPermission,
    getDashboardRoute,

    // Actions
    login,
    logout,
    faceLogin,
    faceLogout,
    refreshToken,
    checkAuth,
    loadPermissions,
    updateUser,
    clearError,
    initializeAuth
  }
}
