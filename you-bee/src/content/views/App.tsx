import Logo from '@/assets/crx.svg'
import { useState, useEffect, useRef } from 'react'
import './App.css'

function App() {
  const [show, setShow] = useState(false)
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([
    { role: 'YouBee', message: "Hello! I'm You-Bee. Ur helpfull youtube Assistant. How i can help you today?" }
  ])
  const [loading, setLoading] = useState(false)

  const messagesEndRef = useRef<HTMLDivElement | null>(null)

  const toggle = () => setShow(!show)

  const getid = () => {
    const url = new URL(window.location.href)
    const id = url.searchParams.get("v") || ""
    return id
  }

  const handleSend = async () => {
    const trimmed = input.trim()
    if (!trimmed) return

    const userMessage = { role: 'user', message: trimmed }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await fetch('http://localhost:8000/ask/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: trimmed, video_id: getid() })
      })

      const data = await response.json()

      const botMessage = {
        role: 'YouBee',
        message: data.answer || 'Sorry, I could not understand.'
      }

      setMessages(prev => [...prev, botMessage])
    } catch (err) {
      console.error('Error:', err)
      setMessages(prev => [...prev, { role: 'YouBee', message: 'Something went wrong. Please try again.' }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') handleSend()
  }

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <div className="bing fixed right-4 bottom-4">
      {show ? (
        <div
          style={{ backgroundColor: 'black' }}
          className="chat relative w-[25vw] shadow-lg rounded-2xl p-4 flex flex-col"
        >
          <div className='header flex justify-between items-start'>

            <h1 className='heading'>You-Bee 😎</h1> 

            <button
              onClick={toggle}
              className="cross text-white font-bold hover:text-red-600"
            >
              ×
            </button>
          </div>

          <div className="mt-8 flex gap-4 flex-col mb-4 overflow-y-auto flex-1">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`p-3 rounded-xl max-w-[85%] ${msg.role === 'user' ? 'user' : 'youbee'
                  }`}
              >
                {msg.message}
              </div>
            ))}
            {loading && (
              <div className="youbee p-3 rounded-xl max-w-[85%]">
                Thinking...
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="mt-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              className="border border-gray-300 p-4 text-2xl w-full rounded-md"
              placeholder="Type your message..."
              disabled={loading}
            />
          </div>
        </div>
      ) : (
        <button onClick={toggle}>
          <img src={Logo} alt="CRXJS logo" className="w-14 h-14" />
        </button>
      )}
    </div>
  )
}

export default App
