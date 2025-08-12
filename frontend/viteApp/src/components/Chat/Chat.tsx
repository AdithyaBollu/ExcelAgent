
import { useState } from "react";
import ChatBox from "../Chatbox/ChatBox.tsx";
import ChatMessages from "../ChatMessages/ChatMessages.tsx";
import './Chat.css';

// Import or define the Message type
interface Message {
    role: string;
    content: string;
}

function Chat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [messageSent, setMessageSent] = useState(false);
  const [generating, setGenerating] = useState(false);

  return (
    <>
      <div className="chat-container">
        
        {!messageSent && (
          <div className="welcome-message">
            <h2>Welcome to the Chat!</h2>
            <p>Start by typing your message below.</p>
          </div>
        )}
        <ChatMessages messages={messages} generating={generating}/>
        <ChatBox messages={messages} setMessages={setMessages} setMessageSent={setMessageSent} setGenerating={setGenerating}/>
      </div>
    </>
  )
}

export default Chat;