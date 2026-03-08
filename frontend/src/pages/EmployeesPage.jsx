import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Users, 
  Plus, 
  Camera, 
  Trash2, 
  Edit, 
  Search,
  Filter,
  Download,
  UserPlus,
  MoreHorizontal
} from 'lucide-react'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { Table, TableActions, StatusBadge } from '../components/ui/Table'
import { Modal } from '../components/ui/Modal'
import { Card } from '../components/ui/Card'

export const EmployeesPage = () => {
  const [employees] = useState([
    {
      id: 1,
      name: 'John Doe',
      email: 'john.doe@company.com',
      employeeId: 'EMP001',
      department: 'Engineering',
      role: 'Software Engineer',
      status: 'active',
      joinDate: '2023-01-15',
      phone: '+1 234-567-8900',
      avatar: 'JD'
    },
    {
      id: 2,
      name: 'Jane Smith',
      email: 'jane.smith@company.com',
      employeeId: 'EMP002',
      department: 'HR',
      role: 'HR Manager',
      status: 'active',
      joinDate: '2022-06-20',
      phone: '+1 234-567-8901',
      avatar: 'JS'
    },
    {
      id: 3,
      name: 'Mike Johnson',
      email: 'mike.johnson@company.com',
      employeeId: 'EMP003',
      department: 'Sales',
      role: 'Sales Representative',
      status: 'active',
      joinDate: '2023-03-10',
      phone: '+1 234-567-8902',
      avatar: 'MJ'
    },
    {
      id: 4,
      name: 'Sarah Williams',
      email: 'sarah.williams@company.com',
      employeeId: 'EMP004',
      department: 'Engineering',
      role: 'UI/UX Designer',
      status: 'active',
      joinDate: '2022-11-05',
      phone: '+1 234-567-8903',
      avatar: 'SW'
    },
    {
      id: 5,
      name: 'Robert Brown',
      email: 'robert.brown@company.com',
      employeeId: 'EMP005',
      department: 'Marketing',
      role: 'Marketing Manager',
      status: 'inactive',
      joinDate: '2022-08-12',
      phone: '+1 234-567-8904',
      avatar: 'RB'
    },
  ])

  const [searchTerm, setSearchTerm] = useState('')
  const [filterDepartment, setFilterDepartment] = useState('all')
  const [showAddModal, setShowAddModal] = useState(false)
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [selectedEmployee, setSelectedEmployee] = useState(null)

  const filteredEmployees = employees.filter((employee) => {
    const matchesSearch = employee.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         employee.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         employee.employeeId.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesDepartment = filterDepartment === 'all' || employee.department === filterDepartment
    return matchesSearch && matchesDepartment
  })

  const departments = ['all', ...new Set(employees.map(emp => emp.department))]

  const handleCaptureFace = (employee) => {
    console.log('Capture face for:', employee.name)
    // Implement face capture logic
  }

  const handleDeleteEmployee = (employee) => {
    setSelectedEmployee(employee)
    setShowDeleteModal(true)
  }

  const confirmDelete = () => {
    console.log('Delete employee:', selectedEmployee?.name)
    setShowDeleteModal(false)
    setSelectedEmployee(null)
  }

  const tableColumns = [
    {
      key: 'employee',
      title: 'Employee',
      render: (value, row) => (
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
            <span className="text-sm font-medium text-primary">
              {row.avatar}
            </span>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-900">{row.name}</p>
            <p className="text-xs text-gray-500">{row.employeeId}</p>
          </div>
        </div>
      )
    },
    {
      key: 'email',
      title: 'Email',
      render: (value) => (
        <p className="text-sm text-gray-900">{value}</p>
      )
    },
    {
      key: 'department',
      title: 'Department',
      render: (value) => (
        <p className="text-sm text-gray-900">{value}</p>
      )
    },
    {
      key: 'role',
      title: 'Role',
      render: (value) => (
        <p className="text-sm text-gray-900">{value}</p>
      )
    },
    {
      key: 'status',
      title: 'Status',
      render: (value) => (
        <StatusBadge status={value} variant="default" />
      )
    },
    {
      key: 'actions',
      title: 'Actions',
      render: (value, row) => (
        <TableActions
          actions={[
            {
              icon: Camera,
              label: 'Capture Face',
              onClick: () => handleCaptureFace(row),
              variant: 'success'
            },
            {
              icon: Edit,
              label: 'Edit',
              onClick: () => console.log('Edit:', row.name),
              variant: 'default'
            },
            {
              icon: Trash2,
              label: 'Delete',
              onClick: () => handleDeleteEmployee(row),
              variant: 'danger'
            }
          ]}
          row={row}
        />
      )
    }
  ]

  const stats = {
    total: employees.length,
    active: employees.filter(emp => emp.status === 'active').length,
    inactive: employees.filter(emp => emp.status === 'inactive').length,
    departments: new Set(employees.map(emp => emp.department)).size
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Employees</h1>
            <p className="text-gray-600 mt-2">
              Manage your team members and their information
            </p>
          </div>
          <Button
            onClick={() => setShowAddModal(true)}
            icon={UserPlus}
          >
            Add Employee
          </Button>
        </div>
      </motion.div>

      {/* Stats Cards */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
      >
        <Card hover>
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
              <Users className="w-6 h-6 text-primary" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Total Employees</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
            </div>
          </div>
        </Card>

        <Card hover>
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
              <Users className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Active</p>
              <p className="text-2xl font-bold text-green-600">{stats.active}</p>
            </div>
          </div>
        </Card>

        <Card hover>
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center">
              <Users className="w-6 h-6 text-red-600" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Inactive</p>
              <p className="text-2xl font-bold text-red-600">{stats.inactive}</p>
            </div>
          </div>
        </Card>

        <Card hover>
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
              <Filter className="w-6 h-6 text-purple-600" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Departments</p>
              <p className="text-2xl font-bold text-purple-600">{stats.departments}</p>
            </div>
          </div>
        </Card>
      </motion.div>

      {/* Filters and Search */}
      <motion.div
        className="bg-white rounded-xl shadow-sm border border-gray-100 p-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
      >
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div className="flex-1 max-w-md">
            <Input
              label="Search employees..."
              placeholder="Search employees..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <div className="flex items-center space-x-4">
            <select
              className="px-4 py-2 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary"
              value={filterDepartment}
              onChange={(e) => setFilterDepartment(e.target.value)}
            >
              {departments.map((dept) => (
                <option key={dept} value={dept}>
                  {dept === 'all' ? 'All Departments' : dept}
                </option>
              ))}
            </select>
            
            <Button variant="secondary" icon={Download}>
              Export
            </Button>
          </div>
        </div>
      </motion.div>

      {/* Employees Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.3 }}
      >
        <Table
          columns={tableColumns}
          data={filteredEmployees}
          emptyMessage="No employees found matching your criteria."
        />
      </motion.div>

      {/* Add Employee Modal */}
      <Modal
        isOpen={showAddModal}
        onClose={() => setShowAddModal(false)}
        title="Add New Employee"
        size="lg"
      >
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Input
              label="Full Name"
              placeholder="Enter employee name"
            />
            <Input
              label="Email Address"
              type="email"
              placeholder="Enter email address"
            />
            <Input
              label="Employee ID"
              placeholder="Enter employee ID"
            />
            <Input
              label="Phone Number"
              placeholder="Enter phone number"
            />
            <Input
              label="Department"
              placeholder="Enter department"
            />
            <Input
              label="Role"
              placeholder="Enter job role"
            />
          </div>
          
          <div className="flex justify-end space-x-4 pt-4 border-t border-gray-200">
            <Button
              variant="secondary"
              onClick={() => setShowAddModal(false)}
            >
              Cancel
            </Button>
            <Button onClick={() => setShowAddModal(false)}>
              Add Employee
            </Button>
          </div>
        </div>
      </Modal>

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        title="Delete Employee"
        size="sm"
      >
        <div className="text-center">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
            <Trash2 className="h-6 w-6 text-red-600" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Delete {selectedEmployee?.name}?
          </h3>
          <p className="text-sm text-gray-500 mb-6">
            This action cannot be undone. This will permanently delete the employee record.
          </p>
          <div className="flex space-x-3">
            <Button
              variant="secondary"
              onClick={() => setShowDeleteModal(false)}
              className="flex-1"
            >
              Cancel
            </Button>
            <Button
              variant="danger"
              onClick={confirmDelete}
              className="flex-1"
            >
              Delete Employee
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
