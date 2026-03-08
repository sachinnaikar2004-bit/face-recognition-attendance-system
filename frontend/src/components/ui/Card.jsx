import React from 'react'
import { motion } from 'framer-motion'

export const Card = ({ 
  children, 
  className = '', 
  hover = false, 
  padding = 'normal',
  ...props 
}) => {
  const paddingClasses = {
    none: '',
    sm: 'p-4',
    normal: 'p-6',
    lg: 'p-8',
    xl: 'p-10'
  }

  const cardClasses = `bg-white rounded-xl shadow-sm border border-gray-100 ${paddingClasses[padding]} ${hover ? 'hover:shadow-md transition-shadow duration-200' : ''} ${className}`

  return (
    <motion.div
      className={cardClasses}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      whileHover={hover ? { y: -2 } : {}}
      {...props}
    >
      {children}
    </motion.div>
  )
}

export const StatCard = ({ 
  title, 
  value, 
  change, 
  changeType = 'neutral',
  icon: Icon,
  color = 'primary',
  className = '',
  ...props 
}) => {
  const colorClasses = {
    primary: 'bg-primary/10 text-primary',
    secondary: 'bg-secondary/10 text-secondary',
    accent: 'bg-accent/10 text-accent',
    danger: 'bg-red-100 text-red-600',
    warning: 'bg-yellow-100 text-yellow-600',
    success: 'bg-green-100 text-green-600'
  }

  const changeColorClasses = {
    increase: 'text-green-600',
    decrease: 'text-red-600',
    neutral: 'text-gray-500'
  }

  return (
    <Card hover className={className} {...props}>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${colorClasses[color]}`}>
            {Icon && <Icon className="w-6 h-6" />}
          </div>
          <div>
            <p className="text-sm font-medium text-gray-600">{title}</p>
            <p className="text-2xl font-bold text-gray-900">{value}</p>
          </div>
        </div>
        {change && (
          <div className={`text-sm font-medium ${changeColorClasses[changeType]}`}>
            {change}
          </div>
        )}
      </div>
    </Card>
  )
}
