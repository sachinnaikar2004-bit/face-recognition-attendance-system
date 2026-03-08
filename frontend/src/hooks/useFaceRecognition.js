import { useState, useCallback, useRef } from 'react'
import { faceApi } from '../api/faceApi'

export const useFaceRecognition = (options = {}) => {
  const {
    detectionInterval = 1000,
    captureDelay = 2000,
    autoDetect = false,
    onFaceDetected,
    onFaceRecognized,
    onError
  } = options

  const [isDetecting, setIsDetecting] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [detectedFaces, setDetectedFaces] = useState([])
  const [recognitionResult, setRecognitionResult] = useState(null)
  const [error, setError] = useState(null)

  const intervalRef = useRef(null)
  const timeoutRef = useRef(null)

  // Detect faces in image
  const detectFaces = useCallback(async (imageData) => {
    setIsProcessing(true)
    setError(null)

    try {
      const response = await faceApi.detectFaces(imageData)
      const { data } = response

      setDetectedFaces(data.data.detections || [])
      
      if (data.data.faces_detected > 0) {
        onFaceDetected?.(data.data)
      }

      return data.data
    } catch (err) {
      const errorMessage = err.response?.data?.error?.message || 'Face detection failed'
      setError(errorMessage)
      onError?.(errorMessage)
      throw err
    } finally {
      setIsProcessing(false)
    }
  }, [onFaceDetected, onError])

  // Recognize face
  const recognizeFace = useCallback(async (imageData) => {
    setIsProcessing(true)
    setError(null)

    try {
      const response = await faceApi.verifyFace(imageData)
      const { data } = response

      setRecognitionResult(data.data)

      if (data.data.verified) {
        onFaceRecognized?.(data.data)
      }

      return data.data
    } catch (err) {
      const errorMessage = err.response?.data?.error?.message || 'Face recognition failed'
      setError(errorMessage)
      onError?.(errorMessage)
      throw err
    } finally {
      setIsProcessing(false)
    }
  }, [onFaceRecognized, onError])

  // Login with face
  const loginWithFace = useCallback(async (imageData) => {
    setIsProcessing(true)
    setError(null)

    try {
      const response = await faceApi.login(imageData)
      const { data } = response

      setRecognitionResult({
        verified: true,
        emp_id: data.data.user.emp_id,
        name: data.data.user.name,
        confidence: 1.0
      })

      return data
    } catch (err) {
      const errorMessage = err.response?.data?.error?.message || 'Face login failed'
      setError(errorMessage)
      onError?.(errorMessage)
      throw err
    } finally {
      setIsProcessing(false)
    }
  }, [onError])

  // Logout with face
  const logoutWithFace = useCallback(async (imageData) => {
    setIsProcessing(true)
    setError(null)

    try {
      const response = await faceApi.logout(imageData)
      const { data } = response

      return data
    } catch (err) {
      const errorMessage = err.response?.data?.error?.message || 'Face logout failed'
      setError(errorMessage)
      onError?.(errorMessage)
      throw err
    } finally {
      setIsProcessing(false)
    }
  }, [onError])

  // Validate face image
  const validateFaceImage = useCallback(async (imageData) => {
    setIsProcessing(true)
    setError(null)

    try {
      const response = await faceApi.validateFaceImage(imageData)
      const { data } = response

      return data.data
    } catch (err) {
      const errorMessage = err.response?.data?.error?.message || 'Face validation failed'
      setError(errorMessage)
      onError?.(errorMessage)
      throw err
    } finally {
      setIsProcessing(false)
    }
  }, [onError])

  // Register face
  const registerFace = useCallback(async (empId, faceImages) => {
    setIsProcessing(true)
    setError(null)

    try {
      const response = await faceApi.registerFace(empId, faceImages)
      const { data } = response

      return data.data
    } catch (err) {
      const errorMessage = err.response?.data?.error?.message || 'Face registration failed'
      setError(errorMessage)
      onError?.(errorMessage)
      throw err
    } finally {
      setIsProcessing(false)
    }
  }, [onError])

  // Start continuous face detection
  const startDetection = useCallback((captureFunction) => {
    if (isDetecting) return

    setIsDetecting(true)

    intervalRef.current = setInterval(async () => {
      try {
        const imageData = captureFunction()
        await detectFaces(imageData)
      } catch (err) {
        console.error('Detection error:', err)
      }
    }, detectionInterval)

    // Auto-stop after capture delay
    if (captureDelay > 0) {
      timeoutRef.current = setTimeout(() => {
        stopDetection()
      }, captureDelay)
    }
  }, [isDetecting, detectionInterval, captureDelay, detectFaces])

  // Stop face detection
  const stopDetection = useCallback(() => {
    setIsDetecting(false)

    if (intervalRef.current) {
      clearInterval(intervalRef.current)
      intervalRef.current = null
    }

    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current)
      timeoutRef.current = null
    }
  }, [])

  // Reset state
  const reset = useCallback(() => {
    stopDetection()
    setDetectedFaces([])
    setRecognitionResult(null)
    setError(null)
    setIsProcessing(false)
  }, [stopDetection])

  // Cleanup on unmount
  const cleanup = useCallback(() => {
    stopDetection()
  }, [stopDetection])

  return {
    // State
    isDetecting,
    isProcessing,
    detectedFaces,
    recognitionResult,
    error,

    // Actions
    detectFaces,
    recognizeFace,
    loginWithFace,
    logoutWithFace,
    validateFaceImage,
    registerFace,
    startDetection,
    stopDetection,
    reset,
    cleanup
  }
}
