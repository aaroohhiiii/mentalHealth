import React, { useRef, useState, useEffect } from 'react'
const uploadIcon = new URL('../public/icons/folder.png', import.meta.url).href

interface UploadAudioProps {
  onUpload: (file: File) => void
}

// Import the audio waves icon
const audioWavesIcon = new URL('../public/icons/audio-waves.png', import.meta.url).href

const UploadAudio: React.FC<UploadAudioProps> = ({ onUpload }) => {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<Blob[]>([])
  
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isRecording, setIsRecording] = useState(false)
  const [recordingTime, setRecordingTime] = useState(0)
  const [recordedAudio, setRecordedAudio] = useState<string | null>(null)
  const [hasPermission, setHasPermission] = useState<boolean | null>(null)

  useEffect(() => {
    let interval: number
    if (isRecording) {
      interval = window.setInterval(() => {
        setRecordingTime(prev => prev + 1)
      }, 1000)
    }
    return () => clearInterval(interval)
  }, [isRecording])

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      setRecordedAudio(null)
    }
  }

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      setHasPermission(true)
      
      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      audioChunksRef.current = []

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' })
        const audioUrl = URL.createObjectURL(audioBlob)
        setRecordedAudio(audioUrl)
        
        // Convert to File
        const audioFile = new File([audioBlob], `recording-${Date.now()}.webm`, {
          type: 'audio/webm',
        })
        setSelectedFile(audioFile)
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop())
      }

      mediaRecorder.start()
      setIsRecording(true)
      setRecordingTime(0)
    } catch (error) {
      console.error('Error accessing microphone:', error)
      setHasPermission(false)
      alert('Unable to access microphone. Please allow microphone permission.')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  const handleUpload = () => {
    if (selectedFile) {
      onUpload(selectedFile)
      setSelectedFile(null)
      setRecordedAudio(null)
      setRecordingTime(0)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <div style={styles.container}>
      {/* Combined Recording and Upload Section */}
      <div style={styles.combinedSection}>
        {/* Recording Section */}
        <div style={styles.recordSection}>
          <div style={styles.iconImage}>
            <img src={audioWavesIcon} alt="Audio Waves" style={styles.iconImg} />
          </div>
          <h3>Record Audio Check-in</h3>
          <p style={styles.description}>
            Record a 5-10 second voice clip about how you're feeling
          </p>

          {!isRecording ? (
            <button onClick={startRecording} style={styles.recordButton}>
              🎤 Start Recording
            </button>
          ) : (
            <div style={styles.recordingActive}>
              <div style={styles.recordingIndicator}>
                <span style={styles.recordingDot}>●</span> Recording...
              </div>
              <div style={styles.timer}>{formatTime(recordingTime)}</div>
              <button onClick={stopRecording} style={styles.stopButton}>
                ⏹️ Stop Recording
              </button>
            </div>
          )}

          {recordedAudio && (
            <div style={styles.audioPreview}>
              <audio controls src={recordedAudio} style={styles.audioPlayer} />
            </div>
          )}
        </div>

        {/* Divider */}
        <div style={styles.divider}>
          <span style={styles.dividerText}>OR</span>
        </div>

        {/* File Upload Section */}
        <div style={styles.uploadBox}>
          <div style={styles.icon}>
            <img src={uploadIcon} alt="upload" style={{
              height:'60px' ,
              width:'60px' ,
            }}/>
          </div>
          <h3>Upload Audio File</h3>
          <p style={styles.description}>
            Upload a saved audio file (.wav, .mp3, .ogg, .flac, .webm)
          </p>

          <input
            ref={fileInputRef}
            type="file"
            accept=".wav,.mp3,.ogg,.flac,.webm"
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
              {hasPermission === false && '❌ Microphone access denied. '}
              Tip: Speak naturally about how you're feeling today
            </p>
          )}
        </div>
      </div>
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
    padding: '2rem',
    background: 'rgba(102, 126, 234, 0.05)',
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '1rem',
  },
  recordSection: {
    textAlign: 'center' as const,
    padding: '1rem',
  },
  uploadBox: {
    textAlign: 'center' as const,
    padding: '1rem',
  },
  icon: {
    fontSize: '3rem',
    marginBottom: '1rem',
  },
  iconImage: {
    marginBottom: '1rem',
    display: 'flex',
    justifyContent: 'center',
  },
  iconImg: {
    width: '80px',
    height: '80px',
    objectFit: 'contain' as const,
  },
  description: {
    color: '#4f4e4eff',
    marginBottom: '1.5rem',
  },
  recordButton: {
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
  recordingActive: {
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
    gap: '1rem',
    marginTop: '1rem',
  },
  recordingIndicator: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    fontSize: '1.1rem',
    color: '#667eea',
    fontWeight: 'bold' as const,
  },
  recordingDot: {
    color: '#ef4444',
    fontSize: '1.5rem',
    animation: 'pulse 1.5s ease-in-out infinite',
  },
  timer: {
    fontSize: '2rem',
    fontWeight: 'bold' as const,
    color: '#667eea',
    fontFamily: 'monospace',
  },
  stopButton: {
    background: '#ef4444',
    color: 'white',
    border: 'none',
    padding: '0.75rem 2rem',
    borderRadius: '8px',
    fontSize: '1rem',
    fontWeight: 'bold' as const,
    cursor: 'pointer' as const,
  },
  audioPreview: {
    marginTop: '1.5rem',
    padding: '1rem',
    background: 'white',
    borderRadius: '8px',
    border: '1px solid #ddd',
  },
  audioPlayer: {
    width: '100%',
    marginTop: '0.5rem',
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
    fontSize: '1rem',
    color: '#4f4e4eff',
    fontStyle: 'italic' as const,
  },
}

export default UploadAudio
