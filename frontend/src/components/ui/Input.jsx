import React from 'react'
import { motion } from 'framer-motion'
import { Eye, EyeOff, Search } from 'lucide-react'

export const Input = ({ 
  label, 
  type = 'text', 
  placeholder, 
  error, 
  className = '', 
  icon: Icon,
  showPasswordToggle = false,
  ...props 
}) => {
  const [showPassword, setShowPassword] = React.useState(false)
  const [isFocused, setIsFocused] = React.useState(false)

  const inputType = type === 'password' && showPassword ? 'text' : type

  return (
    <div className="space-y-2">
      {label && (
        <label className="text-sm font-medium text-gray-700">
          {label}
        </label>
      )}
      <div className="relative">
        {Icon && (
          <div className="absolute left-3 top-1/2 transform -translate-y-1/2">
            <Icon className="w-5 h-5 text-gray-400" />
          </div>
        )}
        <motion.input
          type={inputType}
          placeholder={placeholder}
          className={`w-full px-4 py-3 rounded-xl border ${Icon ? 'pl-12' : 'pl-4'} ${showPasswordToggle ? 'pr-12' : 'pr-4'} bg-white transition-all duration-200 ${
            error 
              ? 'border-red-300 focus:ring-red-500/20 focus:border-red-500' 
              : isFocused 
                ? 'border-primary ring-2 ring-primary/20 focus:border-primary' 
                : 'border-gray-200 hover:border-gray-300'
          } ${className}`}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          whileFocus={{ scale: 1.01 }}
          transition={{ type: 'spring', stiffness: 400, damping: 17 }}
          {...props}
        />
        {showPasswordToggle && (
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
          >
            {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
          </button>
        )}
      </div>
      {error && (
        <motion.p 
          className="text-sm text-red-600"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2 }}
        >
          {error}
        </motion.p>
      )}
    </div>
  )
}

export const SearchInput = ({ placeholder = 'Search...', className = '', ...props }) => (
  <Input
    type="text"
    placeholder={placeholder}
    icon={Search}
    className={className}
    {...props}
  />
)
