import React from 'react'
import { motion } from 'framer-motion'
import { Loader2 } from 'lucide-react'

export const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'md', 
  loading = false, 
  disabled = false, 
  className = '', 
  icon: Icon,
  ...props 
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-xl transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2'
  
  const variants = {
    primary: 'bg-primary hover:bg-primary-dark text-white shadow-sm hover:shadow-md focus:ring-primary/20',
    secondary: 'bg-white hover:bg-gray-50 text-text-primary border border-gray-200 shadow-sm hover:shadow-md focus:ring-primary/20',
    accent: 'bg-accent hover:bg-green-600 text-white shadow-sm hover:shadow-md focus:ring-accent/20',
    danger: 'bg-red-500 hover:bg-red-600 text-white shadow-sm hover:shadow-md focus:ring-red-500/20',
    ghost: 'hover:bg-gray-100 text-gray-600 hover:text-gray-900 focus:ring-gray-500/20'
  }
  
  const sizes = {
    sm: 'py-2 px-3 text-sm',
    md: 'py-2.5 px-4 text-sm',
    lg: 'py-3 px-6 text-base',
    xl: 'py-4 px-8 text-lg'
  }

  const buttonClasses = `${baseClasses} ${variants[variant]} ${sizes[size]} ${disabled || loading ? 'opacity-50 cursor-not-allowed' : ''} ${className}`

  return (
    <motion.button
      className={buttonClasses}
      disabled={disabled || loading}
      whileHover={disabled || loading ? {} : { scale: 1.02 }}
      whileTap={disabled || loading ? {} : { scale: 0.98 }}
      transition={{ type: 'spring', stiffness: 400, damping: 17 }}
      {...props}
    >
      {loading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
      {Icon && !loading && <Icon className="w-4 h-4 mr-2" />}
      {children}
    </motion.button>
  )
}
