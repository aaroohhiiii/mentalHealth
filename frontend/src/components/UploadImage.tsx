import React, { useRef, useState } from 'react'

interface UploadImageProps {
  onUpload: (file: File) => void
}

const UploadImage: React.FC<UploadImageProps> = ({ onUpload }) => {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)

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
      <div style={styles.uploadBox}>
        <div style={styles.icon}>📸</div>
        <h3>Upload Selfie</h3>
        <p style={styles.description}>
          Upload a selfie for facial expression analysis (.jpg, .png)
        </p>

        <input
          ref={fileInputRef}
          type="file"
          accept=".jpg,.jpeg,.png"
          onChange={handleFileSelect}
          style={styles.fileInput}
        />

        {preview && (
          <div style={styles.previewContainer}>
            <img src={preview} alt="Preview" style={styles.preview} />
            <p><strong>{selectedFile?.name}</strong></p>
            <button onClick={handleUpload} style={styles.uploadButton}>
              Analyze Image
            </button>
          </div>
        )}

        {!preview && (
          <p style={styles.hint}>
            Tip: Take 4-5 selfies throughout the day in natural lighting
          </p>
        )}
      </div>
    </div>
  )
}

const styles = {
  container: {
    padding: '1rem',
  },
  uploadBox: {
    border: '2px dashed #667eea',
    borderRadius: '12px',
    padding: '2rem',
    textAlign: 'center' as const,
    background: 'rgba(102, 126, 234, 0.05)',
  },
  icon: {
    fontSize: '3rem',
    marginBottom: '1rem',
  },
  description: {
    color: '#666',
    marginBottom: '1.5rem',
  },
  fileInput: {
    marginBottom: '1rem',
  },
  previewContainer: {
    marginTop: '1rem',
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
}

export default UploadImage
