import React, { useRef, useState } from 'react'

interface UploadAudioProps {
  onUpload: (file: File) => void
}

const UploadAudio: React.FC<UploadAudioProps> = ({ onUpload }) => {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
    }
  }

  const handleUpload = () => {
    if (selectedFile) {
      onUpload(selectedFile)
      setSelectedFile(null)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  return (
    <div style={styles.container}>
      <div style={styles.uploadBox}>
        <div style={styles.icon}>🎤</div>
        <h3>Upload Audio Check-in</h3>
        <p style={styles.description}>
          Upload a 5-10 second voice recording (.wav, .mp3, .ogg, .flac)
        </p>

        <input
          ref={fileInputRef}
          type="file"
          accept=".wav,.mp3,.ogg,.flac"
          onChange={handleFileSelect}
          style={styles.fileInput}
        />

        {selectedFile && (
          <div style={styles.selectedFile}>
            <p>Selected: <strong>{selectedFile.name}</strong></p>
            <p>Size: {(selectedFile.size / 1024).toFixed(2)} KB</p>
            <button onClick={handleUpload} style={styles.uploadButton}>
              Analyze Audio
            </button>
          </div>
        )}

        {!selectedFile && (
          <p style={styles.hint}>
            Tip: Speak naturally about how you're feeling today
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
  selectedFile: {
    marginTop: '1rem',
    padding: '1rem',
    background: 'white',
    borderRadius: '8px',
    border: '1px solid #ddd',
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

export default UploadAudio
