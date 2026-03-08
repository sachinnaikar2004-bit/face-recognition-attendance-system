import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Camera, Mail, Lock, Eye, EyeOff, ArrowRight } from 'lucide-react'
import { useAuthStore } from '../store/authStore'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'

export const LoginPage = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  
  const { login } = useAuthStore()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      await login(email, password)
      navigate('/admin/dashboard')
    } catch (err) {
      setError(err.message || 'Login failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex">
      {/* Left Side - Hero Section */}
      <motion.div
        className="hidden lg:flex lg:w-1/2 gradient-primary relative overflow-hidden"
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.8 }}
      >
        <div className="absolute inset-0 bg-black/20" />
        <div className="relative z-10 flex flex-col justify-center px-12 text-white">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <div className="flex items-center space-x-3 mb-8">
              <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center">
                <Camera className="w-7 h-7" />
              </div>
              <h1 className="text-3xl font-bold">FaceAttend</h1>
            </div>
            
            <h2 className="text-4xl font-bold mb-6">
              Smart Attendance System
            </h2>
            
            <p className="text-xl text-white/90 mb-8 leading-relaxed">
              Experience the future of attendance management with advanced face recognition technology. 
              Track, manage, and analyze employee attendance with precision and ease.
            </p>
            
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-green-400 rounded-full" />
                <span className="text-white/80">AI-powered face recognition</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-green-400 rounded-full" />
                <span className="text-white/80">Real-time attendance tracking</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-green-400 rounded-full" />
                <span className="text-white/80">Advanced analytics dashboard</span>
              </div>
            </div>
          </motion.div>
          
          <motion.div
            className="absolute bottom-12 left-12 right-12"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-2xl font-bold">10,000+</p>
                  <p className="text-white/80">Daily Check-ins</p>
                </div>
                <div>
                  <p className="text-2xl font-bold">99.9%</p>
                  <p className="text-white/80">Accuracy Rate</p>
                </div>
                <div>
                  <p className="text-2xl font-bold">500+</p>
                  <p className="text-white/80">Companies Trust</p>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </motion.div>

      {/* Right Side - Login Form */}
      <motion.div
        className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-white"
        initial={{ opacity: 0, x: 50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.8 }}
      >
        <div className="w-full max-w-md">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-center mb-8"
          >
            <div className="lg:hidden flex items-center justify-center space-x-3 mb-6">
              <div className="w-12 h-12 bg-primary rounded-xl flex items-center justify-center">
                <Camera className="w-7 h-7 text-white" />
              </div>
              <h1 className="text-3xl font-bold text-gray-900">FaceAttend</h1>
            </div>
            
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Welcome Back
            </h2>
            <p className="text-gray-600">
              Sign in to your account to continue
            </p>
          </motion.div>

          <motion.form
            onSubmit={handleSubmit}
            className="space-y-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            {error && (
              <motion.div
                className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-xl"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                {error}
              </motion.div>
            )}

            <Input
              type="email"
              label="Email Address"
              placeholder="Enter your email"
              icon={Mail}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <Input
              type="password"
              label="Password"
              placeholder="Enter your password"
              icon={Lock}
              showPasswordToggle
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            <div className="flex items-center justify-between">
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  className="w-4 h-4 text-primary border-gray-300 rounded focus:ring-primary"
                />
                <span className="text-sm text-gray-600">Remember me</span>
              </label>
              <Link
                to="/forgot-password"
                className="text-sm text-primary hover:text-primary-dark transition-colors"
              >
                Forgot password?
              </Link>
            </div>

            <Button
              type="submit"
              loading={isLoading}
              className="w-full py-3 text-base"
            >
              Sign In
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
          </motion.form>

          <motion.div
            className="mt-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-200" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-4 bg-white text-gray-500">Or continue with</span>
              </div>
            </div>

            <Link
              to="/face-login"
              className="mt-6 w-full flex items-center justify-center px-4 py-3 border-2 border-dashed border-gray-300 rounded-xl text-gray-700 hover:border-primary hover:text-primary transition-all duration-200 group"
            >
              <Camera className="w-5 h-5 mr-2 group-hover:scale-110 transition-transform" />
              Face Recognition Login
            </Link>
          </motion.div>

          <motion.p
            className="mt-8 text-center text-sm text-gray-600"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.5 }}
          >
            Don't have an account?{' '}
            <Link
              to="/register"
              className="font-medium text-primary hover:text-primary-dark transition-colors"
            >
              Contact your administrator
            </Link>
          </motion.p>
        </div>
      </motion.div>
    </div>
  )
}
