
import "./ChatBox.css"
import SendIcon from "../../icons/Send.svg" 
import AttachIcon from "../../icons/Attach.svg"
import { useState, useRef, useEffect } from "react";


interface Message {
    role: string;
    content: string;
}

interface ChatBoxProps {
  messages: Message[];  
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>
  setMessageSent: React.Dispatch<React.SetStateAction<boolean>>;
  setGenerating: React.Dispatch<React.SetStateAction<boolean>>; // Optional if not used
}

const ChatBox : React.FC<ChatBoxProps> = ({messages, setMessages, setMessageSent, setGenerating}) => {
  const textRef = useRef(null);
  const [message, setMessage] = useState("");

  function handleInput(e: React.FormEvent<HTMLTextAreaElement>) {
    const textarea = e.target as HTMLTextAreaElement;
    textarea.style.height = 'auto'; // Reset height to auto to shrink if needed

    setMessage(textarea.value); // Update message state

    const newHeight = Math.min(Math.max(textarea.scrollHeight, 
      parseFloat(getComputedStyle(textarea).minHeight)), 
      parseFloat(getComputedStyle(textarea).maxHeight));
    
    textarea.style.height = `${newHeight}px`; // Set the new height

    if (textarea.scrollHeight > parseFloat(getComputedStyle(textarea).maxHeight)) {
      textarea.style.overflowY = 'auto'; // Enable scroll if content exceeds max height
    } else {
      textarea.style.overflowY = 'hidden'; // Hide scroll if content is within limits
    }
    
  }

  async function handleSend() {
    if (message.trim() === "") return; // Prevent sending empty messages

    try {
      console.log("Sending message:", message);
      setMessageSent(true);
      setGenerating(true);
      const newMessage: Message = {
        role: "user",
        content: message
      };

      
      if (textRef.current) {
        const textarea = textRef.current as HTMLTextAreaElement;
        textarea.value = ""; // Clear the textarea
        textarea.style.height = getComputedStyle(textarea).minHeight; // Reset height
      }

      setMessages(prevMessages => [...prevMessages, newMessage]);
      let res = await fetch ("http://localhost:5000/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ message: message, history: messages })
        });
      
        const data = await res.json();
        const botMessage: Message = {
          role: "assistant",
          content: data.response
        };
        setMessages(prevMessages => [...prevMessages, botMessage]);
        setMessage(""); // Clear the input after sending
         setGenerating(false); // Stop generating state

    } catch (error) {
      console.error("Error sending message:", error);
    }

    // setMessages(prevMessages => [...prevMessages, newMessage]);
    // setMessage(""); // Clear the input after sending

    // Optionally, you can also handle the assistant's response here
    // For example, you could call an API to get the assistant's reply
  }

  useEffect(() => {
    if (textRef.current) {
      const textarea = textRef.current as HTMLTextAreaElement; 
      textarea.style.height = getComputedStyle(textarea).minHeight;
    }
  }, []);

  return (
    <>
      <div className="chat-box-container">
        
        <div className="tools-container">
          <textarea
            className="inp"
            ref={textRef}
            placeholder="Type your message here..."
            onInput={handleInput}
          />
          <div className="tools">
            <button className="sendBtn btn" onClick={handleSend}>
              <img className="send-icon" src={SendIcon} alt="Send" />
            </button>
            <button className="attachBtn btn">
              <img className="attach-icon" src={AttachIcon} alt="Send" />
            </button>
          </div>
        </div>
        
        
        
      </div>
    </>
  )
}

export default ChatBox;