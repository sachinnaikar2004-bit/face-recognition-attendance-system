import { create } from 'zustand'
import { employeeApi } from '../api/employeeApi'

export const useEmployeeStore = create((set, get) => ({
  // State
  employees: [],
  currentEmployee: null,
  employeeStats: null,
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
  fetchEmployees: async (filters = {}) => {
    set({ isLoading: true, error: null })
    try {
      const response = await employeeApi.getEmployees(filters)
      const { data } = response
      
      set({
        employees: data.employees,
        pagination: data.pagination,
        isLoading: false
      })
      
      return data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || 'Failed to fetch employees'
      set({ 
        error: errorMessage,
        isLoading: false 
      })
      throw error
    }
  },

  fetchEmployee: async (empId) => {
    set({ isLoading: true, error: null })
    try {
      const response = await employeeApi.getEmployee(empId)
      const { data } = response
      
      set({
        currentEmployee: data.data,
        isLoading: false
      })
      
      return data.data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || 'Failed to fetch employee'
      set({ 
        error: errorMessage,
        isLoading: false 
      })
      throw error
    }
  },

  createEmployee: async (employeeData) => {
    set({ isLoading: true, error: null })
    try {
      const response = await employeeApi.createEmployee(employeeData)
      const { data } = response
      
      // Add new employee to the list
      set(state => ({
        employees: [data.data, ...state.employees],
        isLoading: false
      }))
      
      return data.data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || 'Failed to create employee'
      set({ 
        error: errorMessage,
        isLoading: false 
      })
      throw error
    }
  },

  updateEmployee: async (empId, updateData) => {
    set({ isLoading: true, error: null })
    try {
      const response = await employeeApi.updateEmployee(empId, updateData)
      const { data } = response
      
      // Update employee in the list
      set(state => ({
        employees: state.employees.map(emp => 
          emp.emp_id === empId ? data.data : emp
        ),
        currentEmployee: state.currentEmployee?.emp_id === empId ? data.data : state.currentEmployee,
        isLoading: false
      }))
      
      return data.data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || 'Failed to update employee'
      set({ 
        error: errorMessage,
        isLoading: false 
      })
      throw error
    }
  },

  deleteEmployee: async (empId) => {
    set({ isLoading: true, error: null })
    try {
      await employeeApi.deleteEmployee(empId)
      
      // Remove employee from the list
      set(state => ({
        employees: state.employees.filter(emp => emp.emp_id !== empId),
        currentEmployee: state.currentEmployee?.emp_id === empId ? null : state.currentEmployee,
        isLoading: false
      }))
      
      return true
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || 'Failed to delete employee'
      set({ 
        error: errorMessage,
        isLoading: false 
      })
      throw error
    }
  },

  recaptureFace: async (empId, faceImage) => {
    set({ isLoading: true, error: null })
    try {
      const response = await employeeApi.recaptureFace(empId, faceImage)
      const { data } = response
      
      // Update employee face encoding status
      set(state => ({
        employees: state.employees.map(emp => 
          emp.emp_id === empId 
            ? { ...emp, has_face_encoding: true }
            : emp
        ),
        currentEmployee: state.currentEmployee?.emp_id === empId 
          ? { ...state.currentEmployee, has_face_encoding: true }
          : state.currentEmployee,
        isLoading: false
      }))
      
      return data.data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || 'Failed to recapture face'
      set({ 
        error: errorMessage,
        isLoading: false 
      })
      throw error
    }
  },

  fetchEmployeeStats: async () => {
    set({ isLoading: true, error: null })
    try {
      const response = await employeeApi.getEmployeeStats()
      const { data } = response
      
      set({
        employeeStats: data.data,
        isLoading: false
      })
      
      return data.data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || 'Failed to fetch employee stats'
      set({ 
        error: errorMessage,
        isLoading: false 
      })
      throw error
    }
  },

  clearCurrentEmployee: () => {
    set({ currentEmployee: null })
  },

  clearError: () => {
    set({ error: null })
  },

  resetStore: () => {
    set({
      employees: [],
      currentEmployee: null,
      employeeStats: null,
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
