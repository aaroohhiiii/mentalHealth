import { useState } from 'react'
import axios from 'axios'
import UploadAudio from '../components/UploadAudio'
import UploadImage from '../components/UploadImage'
import ModalityCard from '../components/ModalityCard'
import analysisIcon from '../public/icons/analysis.png?url'
import cameraIcon from '../public/icons/camera.png?url'
import audioIcon from '../public/icons/audio-waves.png?url'

const API_BASE = 'http://localhost:8000'

function NewEntry() {
  const [textInput, setTextInput] = useState('')
  const [textResult, setTextResult] = useState<any>(null)
  const [audioResult, setAudioResult] = useState<any>(null)
  const [imageResult, setImageResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleTextSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!textInput.trim()) {
      setError('Please enter some text')
      return
    }

    try {
      setLoading(true)
      setError(null)

      const response = await axios.post(`${API_BASE}/analyze/text`, {
        text: textInput,
      })

      setTextResult(response.data)
      setTextInput('')
      alert('Text analyzed successfully!')
    } catch (err: any) {
      console.error('Error analyzing text:', err)
      setError(err.response?.data?.detail || err.message || 'Failed to analyze text')
    } finally {
      setLoading(false)
    }
  }

  const handleAudioUpload = async (file: File) => {
    try {
      setLoading(true)
      setError(null)

      const formData = new FormData()
      formData.append('file', file)

      const response = await axios.post(`${API_BASE}/analyze/audio`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setAudioResult(response.data)
      alert('Audio analyzed successfully!')
    } catch (err: any) {
      console.error('Error analyzing audio:', err)
      setError(err.response?.data?.detail || err.message || 'Failed to analyze audio')
    } finally {
      setLoading(false)
    }
  }

  const handleImageUpload = async (file: File) => {
    try {
      setLoading(true)
      setError(null)

      const formData = new FormData()
      formData.append('file', file)

      const response = await axios.post(`${API_BASE}/analyze/image`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setImageResult(response.data)
      alert('Image analyzed successfully!')
    } catch (err: any) {
      console.error('Error analyzing image:', err)
      setError(err.response?.data?.detail || err.message || 'Failed to analyze image')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      {/* <div className="card"> */}
        <h2 style={{
          display:'flex' ,
          alignItems:'center' ,
          justifyContent:'center' ,
          fontSize : '30px', 
          color:'#ffffffff' ,
          marginBottom:'20px'

        }}> </h2>
        {/* <p>Add daily text logs, voice check-ins, or selfies for mental health monitoring.</p> */}
      

      {error && (
        <div className="error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {loading && <div className="loading">Analyzing...</div>}

      {/* Text Entry */}
      <div className="card">
        <h3 style={{
          display:'flex' ,
          alignItems:'center' ,
          justifyContent:'center' ,
          fontSize : '30px'

        }}>Lets Check In our thoughts for today !</h3>
        <form onSubmit={handleTextSubmit}>
          <textarea
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
            placeholder="How are you feeling today? 
Write about your thoughts, mood, or anything on your mind..."
            style={styles.textarea}
            rows={6}
          />
          <div style={styles.buttonContainer}>
            <button type="submit" disabled={loading} style={styles.submitButton}>
              Analyze Text
            </button>
            <span style={styles.hint}>
              Tip: Everything is gonna be fine ! Be honest and detailed for better insights and sit back :D
            </span>
          </div>
        </form>
      </div>

      {/* Audio Entry */}
      <div className="card">
        <h3> Voice Check-in</h3>
        <UploadAudio onUpload={handleAudioUpload} />
      </div>

      {/* Image Entry */}
      <div className="card">
        <h3> Selfie Analysis</h3>
        <UploadImage onUpload={handleImageUpload} />
      </div>

      {/* Results */}
      {(textResult || audioResult || imageResult) && (
        <>
          <div className="card">
            <h2 style={styles.resultsHeader}>
              <img src={analysisIcon} alt="Analysis" style={styles.headerIcon} />
              Latest Analysis Results
            </h2>
          </div>

          <div style={styles.resultsGrid}>
            {textResult && (
              <ModalityCard
                modality="Text"
                score={textResult.score}
                bucket={textResult.bucket}
                explain={textResult.explain}
                icon={analysisIcon}
              />
            )}
            {audioResult && (
              <ModalityCard
                modality="Audio"
                score={audioResult.score}
                bucket={audioResult.bucket}
                explain={audioResult.explain}
                icon={audioIcon}
              />
            )}
            {imageResult && (
              <ModalityCard
                modality="Image"
                score={imageResult.score}
                bucket={imageResult.bucket}
                explain={imageResult.explain}
                icon={cameraIcon}
              />
            )}
          </div>
        </>
      )}
    </div>
  )
}

const styles = {
  textarea: {
    background: 'linear-gradient(#f9f9f9 0%, #fefefe 100%)',
    backgroundImage: `
      repeating-linear-gradient(
        transparent,
        transparent 31px,
        #e5e5e5 31px,
        #e5e5e5 32px
      ),
      linear-gradient(
        90deg,
        #d4e8f7 0px,
        #d4e8f7 40px,
        transparent 40px
      )
    `,
    color: '#2c3e50',
    width: '100%',
    padding: '1rem 1rem 1rem 50px',
    fontSize: '1.1rem',
    lineHeight: '32px',
    borderRadius: '8px',
    border: '2px solid #6abce2',
    borderLeft: '3px solid #235284',
    fontFamily: "'Kalam', 'Handlee', 'Comic Sans MS', cursive",
    resize: 'vertical' as const,
    marginBottom: '1rem',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1), inset 0 1px 2px rgba(0, 0, 0, 0.05)',
  },
  buttonContainer: {
    
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    flexWrap: 'wrap' as const,
    gap: '1rem',
  },
  submitButton: {
    background: '#5cbeffff',
    color: 'white',
    border: 'none',
    padding: '0.75rem 2rem',
    borderRadius: '8px',
    fontSize: '1rem',
    fontWeight: 'bold' as const,
    cursor: 'pointer' as const,
  },
  hint: {
    fontSize: '0.85rem',
    color: '#999',
    fontStyle: 'italic' as const,
  },
  resultsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '1.5rem',
  },
  resultsHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
  },
  headerIcon: {
    width: '32px',
    height: '32px',
    objectFit: 'contain' as const,
  },
}

export default NewEntry
