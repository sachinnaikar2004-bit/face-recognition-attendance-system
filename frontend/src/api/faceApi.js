import apiClient from './axiosClient'

export const faceApi = {
  // Face login
  login: async (faceImage) => {
    const response = await apiClient.post('/api/v1/face/login', {
      face_image: faceImage
    })
    return response.data
  },

  // Face logout
  logout: async (faceImage) => {
    const response = await apiClient.post('/api/v1/face/logout', {
      face_image: faceImage
    })
    return response.data
  },

  // Register face
  registerFace: async (empId, faceImages) => {
    const response = await apiClient.post('/api/v1/face/register', {
      emp_id: empId,
      face_images: faceImages
    })
    return response.data
  },

  // Verify face
  verifyFace: async (faceImage) => {
    const response = await apiClient.post('/api/v1/face/verify', {
      face_image: faceImage
    })
    return response.data
  },

  // Detect faces in image
  detectFaces: async (faceImage) => {
    const response = await apiClient.post('/api/v1/face/detect', {
      face_image: faceImage
    })
    return response.data
  },

  // Validate face image
  validateFaceImage: async (faceImage) => {
    const response = await apiClient.post('/api/v1/face/validate', {
      face_image: faceImage
    })
    return response.data
  },

  // Get face quality info
  getFaceQualityInfo: async (empId) => {
    const response = await apiClient.get(`/api/v1/face/quality/${empId}`)
    return response.data
  },

  // Remove face encoding
  removeFaceEncoding: async (empId) => {
    const response = await apiClient.delete(`/api/v1/face/remove/${empId}`)
    return response.data
  },

  // Get face recognition stats
  getFaceRecognitionStats: async () => {
    const response = await apiClient.get('/api/v1/face/stats/summary')
    return response.data
  }
}
