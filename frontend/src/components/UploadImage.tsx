import React, { useRef, useState, useEffect } from 'react'
const cameraIcon = new URL('../public/icons/camera.png', import.meta.url).href
const uploadIcon = new URL('../public/icons/folder.png', import.meta.url).href


interface UploadImageProps {
  onUpload: (file: File) => void
}

const UploadImage: React.FC<UploadImageProps> = ({ onUpload }) => {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [isCameraOpen, setIsCameraOpen] = useState(false)
  const [stream, setStream] = useState<MediaStream | null>(null)
  const [hasPermission, setHasPermission] = useState<boolean | null>(null)
  const [isLoadingCamera, setIsLoadingCamera] = useState(false)

  useEffect(() => {
    return () => {
      // Cleanup: stop camera stream on unmount
      if (stream) {
        stream.getTracks().forEach(track => track.stop())
      }
    }
  }, [stream])

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      
      // Generate preview
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const openCamera = async () => {
    setIsLoadingCamera(true)
    try {
      // Request camera access with specific constraints
      const mediaStream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          facingMode: 'user',
          width: { ideal: 640 },
          height: { ideal: 480 }
        },
        audio: false
      })
      
      setHasPermission(true)
      setStream(mediaStream)
      setIsCameraOpen(true)
      
      // Wait for next tick to ensure video element is rendered
      setTimeout(async () => {
        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream
          try {
            // Explicitly play the video
            await videoRef.current.play()
            console.log('Camera started successfully')
          } catch (playError) {
            console.error('Error playing video:', playError)
          }
        }
        setIsLoadingCamera(false)
      }, 100)
      
    } catch (error: any) {
      console.error('Error accessing camera:', error)
      setHasPermission(false)
      setIsLoadingCamera(false)
      
      // Provide more specific error messages
      if (error.name === 'NotAllowedError') {
        alert('Camera permission denied. Please allow camera access in your browser settings.')
      } else if (error.name === 'NotFoundError') {
        alert('No camera found on this device.')
      } else {
        alert('Unable to access camera: ' + error.message)
      }
    }
  }

  const closeCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop())
      setStream(null)
    }
    setIsCameraOpen(false)
  }

  const captureImage = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current
      const canvas = canvasRef.current
      
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      
      const context = canvas.getContext('2d')
      if (context) {
        context.drawImage(video, 0, 0, canvas.width, canvas.height)
        
        canvas.toBlob((blob) => {
          if (blob) {
            const file = new File([blob], `selfie-${Date.now()}.jpg`, {
              type: 'image/jpeg',
            })
            setSelectedFile(file)
            setPreview(canvas.toDataURL('image/jpeg'))
            closeCamera()
          }
        }, 'image/jpeg', 0.95)
      }
    }
  }

  const handleUpload = () => {
    if (selectedFile) {
      onUpload(selectedFile)
      setSelectedFile(null)
      setPreview(null)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  return (
    <div style={styles.container}>
      {/* Preview Section */}
      {preview && (
        <div style={styles.previewContainer}>
          <img src={preview} alt="Preview" style={styles.preview} />
          <p><strong>{selectedFile?.name}</strong></p>
          <button onClick={handleUpload} style={styles.uploadButton}>
            Analyze Image
          </button>
        </div>
      )}

      {/* Combined Camera and Upload Section */}
      {!preview && (
        <div style={styles.combinedSection}>
          {/* Camera Section */}
          <div style={styles.cameraSection}>
            <img src={cameraIcon} alt="Camera" style={styles.icon}  />
            <h3>Take a Selfie</h3>
            <p style={styles.description}>
              Capture a selfie for facial expression analysis
            </p>

            {!isCameraOpen ? (
              <button 
                onClick={openCamera} 
                style={styles.cameraButton}
                disabled={isLoadingCamera}
              >
                {isLoadingCamera ? (
                  <>⏳ Loading Camera...</>
                ) : (
                  <>
                    <img src={cameraIcon} alt="Camera" style={styles.buttonIcon} />
                    Open Camera
                  </>
                )}
              </button>
            ) : (
              <div style={styles.cameraActive}>
                <video 
                  ref={videoRef} 
                  autoPlay 
                  playsInline 
                  muted
                  style={styles.video}
                />
                <div style={styles.cameraControls}>
                  <button onClick={captureImage} style={styles.captureButton}>
                    <img src={cameraIcon} alt="Capture" style={styles.buttonIcon} />
                    Capture
                  </button>
                  <button onClick={closeCamera} style={styles.closeButton}>
                    ✖️ Close
                  </button>
                </div>
              </div>
            )}

            <canvas ref={canvasRef} style={{ display: 'none' }} />
          </div>

          {/* Divider */}
          <div style={styles.divider}>
            <span style={styles.dividerText}>OR</span>
          </div>

          {/* File Upload Section */}
          <div style={styles.uploadBox}>
            <div style={styles.icon}>
              <img src={uploadIcon} style={styles.icon} alt="upload" />
            </div>
            <h3>Upload Image File</h3>
            <p style={styles.description}>
              Upload a saved image file (.jpg, .jpeg, .png)
            </p>

            <input
              ref={fileInputRef}
              type="file"
              accept=".jpg,.jpeg,.png"
              onChange={handleFileSelect}
              style={styles.fileInput}
            />

            <p style={styles.hint}>
              {hasPermission === false && '❌ Camera access denied. '}
              Tip: Take 4-5 selfies throughout the day in natural lighting
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

const styles = {
  container: {
    padding: '1rem',
  },
  combinedSection: {
    border: '2px solid #667eea',
    borderRadius: '12px',
    padding: '1.5rem',
    background: 'rgba(102, 126, 234, 0.05)',
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '0.75rem',
  },
  cameraSection: {
    textAlign: 'center' as const,
    padding: '0.5rem',
  },
  uploadBox: {
    textAlign: 'center' as const,
    padding: '0.5rem',
  },
 icon: {
    height:'80px',
    width :'80px',
    fontSize: '3rem',
    marginBottom: '1rem',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    margin: '0 auto 1rem auto',
  },
  description: {
    color: '#666',
    marginBottom: '1.5rem',
  },
  cameraButton: {
    background: '#667eea',
    color: 'white',
    border: 'none',
    padding: '0.75rem 2rem',
    borderRadius: '8px',
    fontSize: '1rem',
    fontWeight: 'bold' as const,
    cursor: 'pointer' as const,
    marginTop: '1rem',
  },
  cameraActive: {
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
    gap: '1rem',
    marginTop: '1rem',
  },
  video: {
    width: '100%',
    maxWidth: '480px',
    borderRadius: '12px',
    border: '2px solid #667eea',
    background: '#000',
  },
  cameraControls: {
    display: 'flex',
    gap: '1rem',
    justifyContent: 'center',
  },
  captureButton: {
    background: '#667eea',
    color: 'white',
    border: 'none',
    padding: '0.75rem 2rem',
    borderRadius: '8px',
    fontSize: '1rem',
    fontWeight: 'bold' as const,
    cursor: 'pointer' as const,
  },
  closeButton: {
    background: '#ef4444',
    color: 'white',
    border: 'none',
    padding: '0.75rem 2rem',
    borderRadius: '8px',
    fontSize: '1rem',
    fontWeight: 'bold' as const,
    cursor: 'pointer' as const,
  },
  divider: {
    display: 'flex',
    alignItems: 'center',
    textAlign: 'center' as const,
    margin: '1.5rem 0',
  },
  dividerText: {
    padding: '0 1rem',
    color: '#667eea',
    fontWeight: 'bold' as const,
    fontSize: '1.1rem',
    width: '100%',
  },
  fileInput: {
    marginBottom: '1rem',
  },
  previewContainer: {
    marginTop: '1rem',
    textAlign: 'center' as const,
    padding: '1.5rem',
    background: 'white',
    borderRadius: '12px',
    border: '2px solid #667eea',
  },
  preview: {
    maxWidth: '300px',
    maxHeight: '300px',
    borderRadius: '8px',
    marginBottom: '1rem',
    border: '2px solid #ddd',
  },
  uploadButton: {
    marginTop: '1rem',
    background: '#667eea',
    color: 'white',
    border: 'none',
    padding: '0.75rem 2rem',
    borderRadius: '8px',
    fontSize: '1rem',
    fontWeight: 'bold' as const,
    cursor: 'pointer' as const,
  },
  hint: {
    marginTop: '1rem',
    fontSize: '0.85rem',
    color: '#999',
    fontStyle: 'italic' as const,
  },
  buttonIcon: {
    width: '20px',
    height: '20px',
    objectFit: 'contain' as const,
    marginRight: '0.5rem',
    verticalAlign: 'middle',
  },
}

export default UploadImage
