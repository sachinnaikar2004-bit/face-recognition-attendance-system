import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { authApi } from '../api/authApi'

export const useAuthStore = create(
  persist(
    (set, get) => ({
      // State
      user: null,
      isAuthenticated: false,
      isLoading: false,
      permissions: [],

      // Actions
      login: async (loginData) => {
        set({ isLoading: true })
        try {
          const { data } = loginData
          
          // Store tokens
          localStorage.setItem('access_token', data.access_token)
          localStorage.setItem('refresh_token', data.refresh_token)
          
          // Set user data
          set({
            user: data.user,
            isAuthenticated: true,
            isLoading: false
          })
          
          return { success: true, data }
        } catch (error) {
          set({ isLoading: false })
          return { 
            success: false, 
            error: error.response?.data?.error?.message || 'Login failed' 
          }
        }
      },

      logout: async () => {
        try {
          // Call logout API
          await authApi.logout()
        } catch (error) {
          console.error('Logout API error:', error)
        } finally {
          // Clear local storage and state
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          
          set({
            user: null,
            isAuthenticated: false,
            permissions: []
          })
        }
      },

      refreshToken: async () => {
        const refreshToken = localStorage.getItem('refresh_token')
        if (!refreshToken) {
          get().logout()
          return false
        }

        try {
          const response = await authApi.refreshToken(refreshToken)
          const { data } = response
          
          // Update access token
          localStorage.setItem('access_token', data.access_token)
          
          return true
        } catch (error) {
          get().logout()
          return false
        }
      },

      checkAuth: async () => {
        const token = localStorage.getItem('access_token')
        if (!token) {
          return false
        }

        set({ isLoading: true })
        try {
          const response = await authApi.getCurrentUser()
          const { data } = response
          
          set({
            user: data.data,
            isAuthenticated: true,
            isLoading: false
          })
          
          return true
        } catch (error) {
          // Try to refresh token
          const refreshed = await get().refreshToken()
          if (!refreshed) {
            get().logout()
            return false
          }
          
          // Retry getting current user
          try {
            const retryResponse = await authApi.getCurrentUser()
            const { data } = retryResponse
            
            set({
              user: data.data,
              isAuthenticated: true,
              isLoading: false
            })
            
            return true
          } catch (retryError) {
            get().logout()
            return false
          }
        }
      },

      loadPermissions: async () => {
        try {
          const response = await authApi.getPermissions()
          const { data } = response
          
          set({ permissions: data.data.permissions })
          return data.data.permissions
        } catch (error) {
          console.error('Failed to load permissions:', error)
          return []
        }
      },

      updateUser: (userData) => {
        set(state => ({
          user: { ...state.user, ...userData }
        }))
      },

      clearError: () => {
        // This can be used to clear any error state
        set({ isLoading: false })
      }
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
        permissions: state.permissions
      })
    }
  )
)
