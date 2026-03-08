import { create } from 'zustand'
import { attendanceApi } from '../api/attendanceApi'

export const useAttendanceStore = create((set, get) => ({
  // State
  attendanceRecords: [],
  todayAttendance: [],
  attendanceStats: null,
  employeeAttendanceHistory: null,
  isLoading: false,
  error: null,
  pagination: {
    page: 1,
    limit: 10,
    total: 0,
    pages: 0,
    has_next: false,
    has_prev: false
  },

  // Actions
  fetchAttendance: async (filters = {}) => {
    set({ isLoading: true, error: null })
    try {
      const response = await attendanceApi.getAttendance(filters)
      const { data } = response
      
      set({
        attendanceRecords: data.attendance,
        pagination: data.pagination,
        isLoading: false
      })
      
      return data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || 'Failed to fetch attendance'
      set({ 
        error: errorMessage,
        isLoading: false 
      })
      throw error
    }
  },

  fetchTodayAttendance: async () => {
    set({ isLoading: true, error: null })
    try {
      const response = await attendanceApi.getTodayAttendance()
      const { data } = response
      
      set({
        todayAttendance: data.records,
        isLoading: false
      })
      
      return data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || 'Failed to fetch today\'s attendance'
      set({ 
        error: errorMessage,
        isLoading: false 
      })
      throw error
    }
  },

  fetchAttendanceByDate: async (date) => {
    set({ isLoading: true, error: null })
    try {
      const response = await attendanceApi.getAttendanceByDate(date)
      const { data } = response
      
      set({
        attendanceRecords: data.records,
        isLoading: false
      })
      
      return data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || 'Failed to fetch attendance for date'
      set({ 
        error: errorMessage,
        isLoading: false 
      })
      throw error
    }
  },

  fetchEmployeeAttendanceHistory: async (empId, days = 30) => {
    set({ isLoading: true, error: null })
    try {
      const response = await attendanceApi.getEmployeeAttendanceHistory(empId, days)
      const { data } = response
      
      set({
        employeeAttendanceHistory: data,
        isLoading: false
      })
      
      return data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || 'Failed to fetch employee attendance history'
      set({ 
        error: errorMessage,
        isLoading: false 
      })
      throw error
    }
  },

  fetchAttendanceStats: async (period = 'month') => {
    set({ isLoading: true, error: null })
    try {
      const response = await attendanceApi.getAttendanceStats(period)
      const { data } = response
      
      set({
        attendanceStats: data.data,
        isLoading: false
      })
      
      return data.data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || 'Failed to fetch attendance statistics'
      set({ 
        error: errorMessage,
        isLoading: false 
      })
      throw error
    }
  },

  markAttendance: async (attendanceType) => {
    set({ isLoading: true, error: null })
    try {
      const response = await attendanceApi.markAttendance(attendanceType)
      const { data } = response
      
      // Update today's attendance if it exists
      if (attendanceType === 'login') {
        set(state => ({
          todayAttendance: [data.data, ...state.todayAttendance],
          isLoading: false
        }))
      } else if (attendanceType === 'logout') {
        set(state => ({
          todayAttendance: state.todayAttendance.map(record =>
            record.emp_id === data.data.emp_id ? data.data : record
          ),
          isLoading: false
        }))
      }
      
      return data.data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || 'Failed to mark attendance'
      set({ 
        error: errorMessage,
        isLoading: false 
      })
      throw error
    }
  },

  exportAttendance: async (filters = {}) => {
    set({ isLoading: true, error: null })
    try {
      await attendanceApi.exportAttendance(filters)
      set({ isLoading: false })
      return true
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || 'Failed to export attendance'
      set({ 
        error: errorMessage,
        isLoading: false 
      })
      throw error
    }
  },

  refreshTodayAttendance: () => {
    get().fetchTodayAttendance()
  },

  clearEmployeeHistory: () => {
    set({ employeeAttendanceHistory: null })
  },

  clearError: () => {
    set({ error: null })
  },

  resetStore: () => {
    set({
      attendanceRecords: [],
      todayAttendance: [],
      attendanceStats: null,
      employeeAttendanceHistory: null,
      error: null,
      pagination: {
        page: 1,
        limit: 10,
        total: 0,
        pages: 0,
        has_next: false,
        has_prev: false
      }
    })
  }
}))
