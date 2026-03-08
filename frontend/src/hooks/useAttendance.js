import { useCallback } from 'react'
import { useAttendanceStore } from '../store/attendanceStore'
import { useAuth } from './useAuth'

export const useAttendance = () => {
  const {
    attendanceRecords,
    todayAttendance,
    attendanceStats,
    employeeAttendanceHistory,
    isLoading,
    error,
    pagination,
    fetchAttendance,
    fetchTodayAttendance,
    fetchAttendanceByDate,
    fetchEmployeeAttendanceHistory,
    fetchAttendanceStats,
    markAttendance,
    exportAttendance,
    refreshTodayAttendance,
    clearEmployeeHistory,
    clearError,
    resetStore
  } = useAttendanceStore()

  const { user, isAdmin, isEmployee } = useAuth()

  // Fetch attendance based on user role
  const fetchUserAttendance = useCallback(async (filters = {}) => {
    if (isAdmin()) {
      // Admin can see all attendance
      return await fetchAttendance(filters)
    } else if (isEmployee()) {
      // Employee can only see their own attendance
      return await fetchAttendance({ ...filters, emp_id: user.emp_id })
    }
  }, [fetchAttendance, isAdmin, isEmployee, user])

  // Fetch today's attendance
  const fetchTodayUserAttendance = useCallback(async () => {
    return await fetchTodayAttendance()
  }, [fetchTodayAttendance])

  // Mark attendance (login/logout)
  const markUserAttendance = useCallback(async (attendanceType) => {
    if (!isEmployee()) {
      throw new Error('Only employees can mark attendance')
    }
    return await markAttendance(attendanceType)
  }, [markAttendance, isEmployee])

  // Export attendance based on user role
  const exportUserAttendance = useCallback(async (filters = {}) => {
    if (isAdmin()) {
      // Admin can export all attendance
      return await exportAttendance(filters)
    } else if (isEmployee()) {
      // Employee can only export their own attendance
      return await exportAttendance({ ...filters, emp_id: user.emp_id })
    }
  }, [exportAttendance, isAdmin, isEmployee, user])

  // Get attendance summary for today
  const getTodaySummary = useCallback(() => {
    const summary = {
      total: todayAttendance.length,
      present: 0,
      absent: 0,
      active: 0
    }

    todayAttendance.forEach(record => {
      if (record.status === 'present') {
        summary.present++
      } else if (record.status === 'absent') {
        summary.absent++
      }
      
      if (record.is_active_session) {
        summary.active++
      }
    })

    return summary
  }, [todayAttendance])

  // Get user's attendance statistics
  const getUserStats = useCallback(() => {
    if (!attendanceStats) return null

    if (isAdmin()) {
      return attendanceStats
    } else if (isEmployee()) {
      // For employees, return simplified stats
      return {
        period: attendanceStats.period,
        present_today: todayAttendance.filter(r => r.status === 'present').length,
        personal_attendance_rate: 0 // Would need to calculate from personal data
      }
    }
  }, [attendanceStats, isAdmin, isEmployee, todayAttendance])

  // Check if user is currently logged in
  const isUserLoggedIn = useCallback(() => {
    if (!isEmployee() || !user) return false
    
    const userAttendance = todayAttendance.find(record => record.emp_id === user.emp_id)
    return userAttendance?.is_active_session || false
  }, [todayAttendance, isEmployee, user])

  // Get user's login time for today
  const getUserLoginTime = useCallback(() => {
    if (!isEmployee() || !user) return null
    
    const userAttendance = todayAttendance.find(record => record.emp_id === user.emp_id)
    return userAttendance?.login_time || null
  }, [todayAttendance, isEmployee, user])

  // Get user's work duration for today
  const getUserWorkDuration = useCallback(() => {
    if (!isEmployee() || !user) return null
    
    const userAttendance = todayAttendance.find(record => record.emp_id === user.emp_id)
    return userAttendance?.duration || null
  }, [todayAttendance, isEmployee, user])

  return {
    // State
    attendanceRecords,
    todayAttendance,
    attendanceStats,
    employeeAttendanceHistory,
    isLoading,
    error,
    pagination,

    // Computed
    getTodaySummary,
    getUserStats,
    isUserLoggedIn,
    getUserLoginTime,
    getUserWorkDuration,

    // Actions
    fetchAttendance: fetchUserAttendance,
    fetchTodayAttendance: fetchTodayUserAttendance,
    fetchAttendanceByDate,
    fetchEmployeeAttendanceHistory,
    fetchAttendanceStats,
    markAttendance: markUserAttendance,
    exportAttendance: exportUserAttendance,
    refreshTodayAttendance,
    clearEmployeeHistory,
    clearError,
    resetStore
  }
}
