import React, { useState } from 'react'

export const AttendancePage = () => {
  const [attendanceRecords] = useState([
    {
      id: 1,
      employeeName: 'John Doe',
      employeeId: 'EMP001',
      date: '2024-01-15',
      checkIn: '9:00 AM',
      checkOut: '5:30 PM',
      status: 'present',
      totalHours: '8h 30m',
    },
    {
      id: 2,
      employeeName: 'Jane Smith',
      employeeId: 'EMP002',
      date: '2024-01-15',
      checkIn: '9:15 AM',
      checkOut: '5:45 PM',
      status: 'late',
      totalHours: '8h 30m',
    },
    {
      id: 3,
      employeeName: 'Mike Johnson',
      employeeId: 'EMP003',
      date: '2024-01-15',
      checkIn: '-',
      checkOut: '-',
      status: 'absent',
      totalHours: '0h',
    },
    {
      id: 4,
      employeeName: 'Sarah Williams',
      employeeId: 'EMP004',
      date: '2024-01-15',
      checkIn: '8:45 AM',
      checkOut: '5:15 PM',
      status: 'present',
      totalHours: '8h 30m',
    },
  ])

  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0])
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')

  const filteredRecords = attendanceRecords.filter((record) => {
    const matchesSearch = record.employeeName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         record.employeeId.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = filterStatus === 'all' || record.status === filterStatus
    return matchesSearch && matchesStatus
  })

  const stats = {
    total: attendanceRecords.length,
    present: attendanceRecords.filter(r => r.status === 'present').length,
    late: attendanceRecords.filter(r => r.status === 'late').length,
    absent: attendanceRecords.filter(r => r.status === 'absent').length,
  }

  const exportToCSV = () => {
    const headers = ['Employee Name', 'Employee ID', 'Date', 'Check In', 'Check Out', 'Status', 'Total Hours']
    const csvContent = [
      headers.join(','),
      ...filteredRecords.map(record => [
        record.employeeName,
        record.employeeId,
        record.date,
        record.checkIn,
        record.checkOut,
        record.status,
        record.totalHours,
      ].join(','))
    ].join('\n')

    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `attendance_${selectedDate}.csv`
    a.click()
    window.URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6">
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h1 className="text-xl font-semibold text-gray-900">Attendance Management</h1>
          <p className="mt-2 text-sm text-gray-700">
            View and manage employee attendance records.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                  <div className="w-4 h-4 bg-white rounded-sm"></div>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Total Employees</dt>
                  <dd className="text-lg font-semibold text-gray-900">{stats.total}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
                  <div className="w-4 h-4 bg-white rounded-sm"></div>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Present</dt>
                  <dd className="text-lg font-semibold text-green-600">{stats.present}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-yellow-500 rounded-md flex items-center justify-center">
                  <div className="w-4 h-4 bg-white rounded-sm"></div>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Late</dt>
                  <dd className="text-lg font-semibold text-yellow-600">{stats.late}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-red-500 rounded-md flex items-center justify-center">
                  <div className="w-4 h-4 bg-white rounded-sm"></div>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Absent</dt>
                  <dd className="text-lg font-semibold text-red-600">{stats.absent}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
            <div className="flex-1 min-w-0">
              <h2 className="text-lg font-medium text-gray-900">Attendance Records</h2>
            </div>
            <div className="mt-4 sm:mt-0 flex space-x-3">
              <button
                onClick={exportToCSV}
                className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Export CSV
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div>
              <label htmlFor="date" className="block text-sm font-medium text-gray-700">
                Date
              </label>
              <input
                type="date"
                id="date"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="search" className="block text-sm font-medium text-gray-700">
                Search
              </label>
              <input
                type="text"
                id="search"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                placeholder="Search by name or ID"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="status" className="block text-sm font-medium text-gray-700">
                Status
              </label>
              <select
                id="status"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
              >
                <option value="all">All Status</option>
                <option value="present">Present</option>
                <option value="late">Late</option>
                <option value="absent">Absent</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {filteredRecords.map((record) => (
            <li key={record.id}>
              <div className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <div className="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center">
                        <span className="text-sm font-medium text-primary-600">
                          {record.employeeName.split(' ').map(n => n[0]).join('')}
                        </span>
                      </div>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-900">{record.employeeName}</p>
                      <p className="text-sm text-gray-500">{record.employeeId}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="text-right">
                      <p className="text-sm text-gray-900">{record.checkIn}</p>
                      <p className="text-xs text-gray-500">Check In</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-900">{record.checkOut}</p>
                      <p className="text-xs text-gray-500">Check Out</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium text-gray-900">{record.totalHours}</p>
                      <p className="text-xs text-gray-500">Total Hours</p>
                    </div>
                    <div>
                      <span
                        className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          record.status === 'present'
                            ? 'bg-green-100 text-green-800'
                            : record.status === 'late'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-red-100 text-red-800'
                        }`}
                      >
                        {record.status}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </li>
          ))}
        </ul>
        {filteredRecords.length === 0 && (
          <div className="text-center py-12">
            <p className="text-sm text-gray-500">No attendance records found matching your criteria.</p>
          </div>
        )}
      </div>
    </div>
  )
}
