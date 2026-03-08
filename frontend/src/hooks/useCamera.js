import { useState, useRef, useCallback, useEffect } from 'react'

export const useCamera = (options = {}) => {
  const {
    width = 640,
    height = 480,
    facingMode = 'user',
    autoStart = true
  } = options

  const [isStreaming, setIsStreaming] = useState(false)
  const [error, setError] = useState(null)
  const [devices, setDevices] = useState([])
  const [currentDevice, setCurrentDevice] = useState(null)

  const videoRef = useRef(null)
  const streamRef = useRef(null)
  const canvasRef = useRef(null)

  // Get available camera devices
  const getDevices = useCallback(async () => {
    try {
      const devices = await navigator.mediaDevices.enumerateDevices()
      const videoDevices = devices.filter(device => device.kind === 'videoinput')
      setDevices(videoDevices)
      
      // Set default device if none selected
      if (!currentDevice && videoDevices.length > 0) {
        setCurrentDevice(videoDevices[0].deviceId)
      }
      
      return videoDevices
    } catch (err) {
      setError('Failed to get camera devices')
      console.error('Error getting devices:', err)
      return []
    }
  }, [currentDevice])

  // Start camera stream
  const startStream = useCallback(async (deviceId = null) => {
    try {
      setError(null)
      
      const constraints = {
        video: {
          width: { ideal: width },
          height: { ideal: height },
          facingMode: facingMode,
          deviceId: deviceId ? { exact: deviceId } : undefined
        },
        audio: false
      }

      const stream = await navigator.mediaDevices.getUserMedia(constraints)
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream
        streamRef.current = stream
        setIsStreaming(true)
      }

      return stream
    } catch (err) {
      let errorMessage = 'Failed to access camera'
      
      switch (err.name) {
        case 'NotAllowedError':
          errorMessage = 'Camera permission denied. Please allow camera access.'
          break
        case 'NotFoundError':
          errorMessage = 'No camera found. Please connect a camera.'
          break
        case 'NotReadableError':
          errorMessage = 'Camera is already in use by another application.'
          break
        case 'OverconstrainedError':
          errorMessage = 'Camera constraints not satisfied.'
          break
        default:
          errorMessage = `Camera error: ${err.message}`
      }
      
      setError(errorMessage)
      console.error('Camera error:', err)
      throw err
    }
  }, [width, height, facingMode])

  // Stop camera stream
  const stopStream = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop())
      streamRef.current = null
    }
    
    if (videoRef.current) {
      videoRef.current.srcObject = null
    }
    
    setIsStreaming(false)
  }, [])

  // Switch camera device
  const switchDevice = useCallback(async (deviceId) => {
    stopStream()
    setCurrentDevice(deviceId)
    await startStream(deviceId)
  }, [stopStream, startStream])

  // Capture frame from video
  const captureFrame = useCallback((format = 'jpeg', quality = 0.9) => {
    if (!videoRef.current || !isStreaming) {
      throw new Error('Camera is not streaming')
    }

    const video = videoRef.current
    const canvas = canvasRef.current || document.createElement('canvas')
    canvasRef.current = canvas

    // Set canvas dimensions to match video
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight

    // Draw video frame to canvas
    const ctx = canvas.getContext('2d')
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

    // Convert to base64
    return canvas.toDataURL(`image/${format}`, quality)
  }, [isStreaming])

  // Get video dimensions
  const getVideoDimensions = useCallback(() => {
    if (!videoRef.current) return null
    
    return {
      width: videoRef.current.videoWidth,
      height: videoRef.current.videoHeight
    }
  }, [])

  // Check if camera is supported
  const isSupported = useCallback(() => {
    return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)
  }, [])

  // Initialize camera on mount
  useEffect(() => {
    if (autoStart && isSupported()) {
      getDevices().then(devices => {
        if (devices.length > 0) {
          startStream(currentDevice || devices[0].deviceId)
        }
      })
    }

    return () => {
      stopStream()
    }
  }, [autoStart, isSupported, getDevices, startStream, stopStream, currentDevice])

  // Handle device changes
  useEffect(() => {
    const handleDeviceChange = () => {
      getDevices()
    }

    navigator.mediaDevices.addEventListener('devicechange', handleDeviceChange)
    
    return () => {
      navigator.mediaDevices.removeEventListener('devicechange', handleDeviceChange)
    }
  }, [getDevices])

  return {
    // Refs
    videoRef,
    canvasRef,
    
    // State
    isStreaming,
    error,
    devices,
    currentDevice,
    
    // Actions
    startStream,
    stopStream,
    switchDevice,
    captureFrame,
    getVideoDimensions,
    getDevices,
    
    // Utilities
    isSupported
  }
}
