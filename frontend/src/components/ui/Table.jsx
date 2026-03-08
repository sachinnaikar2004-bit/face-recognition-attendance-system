import React from 'react'
import { motion } from 'framer-motion'
import { ChevronUp, ChevronDown, MoreHorizontal } from 'lucide-react'

export const Table = ({ 
  columns, 
  data, 
  loading = false, 
  emptyMessage = 'No data available',
  className = '',
  ...props 
}) => {
  return (
    <div className={`bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden ${className}`}>
      <div className="overflow-x-auto">
        <table className="w-full" {...props}>
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              {columns.map((column) => (
                <th
                  key={column.key}
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  <div className="flex items-center space-x-1">
                    <span>{column.title}</span>
                    {column.sortable && (
                      <div className="flex flex-col">
                        <ChevronUp className="w-3 h-3 text-gray-400" />
                        <ChevronDown className="w-3 h-3 text-gray-400 -mt-1" />
                      </div>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {loading ? (
              <tr>
                <td colSpan={columns.length} className="px-6 py-12 text-center">
                  <div className="flex items-center justify-center space-x-2">
                    <div className="w-5 h-5 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
                    <span className="text-gray-500">Loading...</span>
                  </div>
                </td>
              </tr>
            ) : data.length === 0 ? (
              <tr>
                <td colSpan={columns.length} className="px-6 py-12 text-center">
                  <div className="text-gray-500">{emptyMessage}</div>
                </td>
              </tr>
            ) : (
              data.map((row, index) => (
                <motion.tr
                  key={row.id || index}
                  className="hover:bg-gray-50 transition-colors"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.2, delay: index * 0.05 }}
                >
                  {columns.map((column) => (
                    <td key={column.key} className="px-6 py-4 whitespace-nowrap">
                      {column.render ? column.render(row[column.key], row) : row[column.key]}
                    </td>
                  ))}
                </motion.tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export const TableActions = ({ actions, row }) => (
  <div className="flex items-center space-x-2">
    {actions.map((action, index) => (
      <button
        key={index}
        onClick={() => action.onClick(row)}
        className={`p-2 rounded-lg transition-colors ${
          action.variant === 'danger'
            ? 'hover:bg-red-50 text-red-600'
            : action.variant === 'success'
            ? 'hover:bg-green-50 text-green-600'
            : 'hover:bg-gray-100 text-gray-600'
        }`}
        title={action.label}
      >
        <action.icon className="w-4 h-4" />
      </button>
    ))}
  </div>
)

export const StatusBadge = ({ status, variant = 'default' }) => {
  const variants = {
    default: {
      active: 'bg-green-100 text-green-800',
      inactive: 'bg-gray-100 text-gray-800',
      pending: 'bg-yellow-100 text-yellow-800',
    },
    attendance: {
      present: 'bg-green-100 text-green-800',
      absent: 'bg-red-100 text-red-800',
      late: 'bg-yellow-100 text-yellow-800',
      'on-time': 'bg-green-100 text-green-800',
      completed: 'bg-blue-100 text-blue-800',
    }
  }

  const statusClasses = variants[variant][status] || 'bg-gray-100 text-gray-800'

  return (
    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${statusClasses}`}>
      {status.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
    </span>
  )
}
