import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Chat from './components/Chat/Chat.tsx'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className='container'>
        {/* <h1>
          Hello World!
        </h1> */}
        <Chat/>
      </div>
    </>
  )
}

export default App
