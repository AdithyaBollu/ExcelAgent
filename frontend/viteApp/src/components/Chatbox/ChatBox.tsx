
import "./ChatBox.css"
import SendIcon from "../../icons/Send.svg" 
import AttachIcon from "../../icons/Attach.svg"
import { useState, useRef, useEffect } from "react";

function ChatBox({setMessages}) {
  const textRef = useRef(null);

  function handleInput(e: React.FormEvent<HTMLTextAreaElement>) {
    const textarea = e.target as HTMLTextAreaElement;
    textarea.style.height = 'auto'; // Reset height to auto to shrink if needed

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
            <button className="sendBtn btn">
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