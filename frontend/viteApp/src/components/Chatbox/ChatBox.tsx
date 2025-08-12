
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
  const textRef = useRef<HTMLTextAreaElement>(null);
  const fileRef = useRef<HTMLInputElement>(null);
  const [files, setFiles] = useState<File[]>([]);
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

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files) {
      const fileArray = Array.from(files);
      setFiles(fileArray);
      // Optionally, you can also handle the files here
      console.log("Files selected:", fileArray);
    }
  }

  async function handleSend() {
    console.log("Message:", message);
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

  async function handleSendWithFiles() {
    console.log("Files:", files);
    // if (message.trim() === "" ) return; // Prevent sending empty messages or without files

    try {
      console.log("Sending message with files:", message, files);
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

      const formData = new FormData();

      formData.append("message", message);
      formData.append("history", JSON.stringify(messages));
      console.log("Files length:", files.length);
      formData.append("file_count", files.length.toString());

      files.forEach((file, index) => {
        formData.append(`file_${index}`, file);
      });

      // formData.append("fileCount", files.length.toString());

      let res = await fetch("http://localhost:5000/chat-with-files", {
        method: "POST",
        body: formData
      });


      const data = await res.json();
      const botMessage: Message = {
        role: "assistant",
        content: data.response
      };
      
      setMessages(prevMessages => [...prevMessages, botMessage]);
      setMessage(""); // Clear the input after sending
      setFiles([]); // Clear files after sending
      setGenerating(false); // Stop generating state

      // Handle file upload logic here if needed

    } catch (error) {
      console.error("Error sending message with files:", error);
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
          <div className="input-container">
            <textarea
            className="inp"
            ref={textRef}
            placeholder="Type your message here..."
            onInput={handleInput}
          />
          <div className="file-list">
            {files.length > 0 && (
              <div className="file-list-ul">
                {files.map((file, index) => (
                  <div key={index} className="file-list-item">
                    {file.name}
                    <button className="remove-file-btn" onClick={() => {
                      setFiles(prevFiles => prevFiles.filter((_, i) => i !== index));
                    }}>X</button>
                  </div>
                ))}
              </div>
            )}
          </div>
          </div>
          
          <div className="tools">
            <button className="sendBtn btn" onClick={() => files.length === 0 ? handleSend() : handleSendWithFiles()}>
              <img className="send-icon" src={SendIcon} alt="Send" />
            </button>
            <input type="file" ref={fileRef} onChange={handleFileChange} multiple accept=".pdf,.txt,.csv,.xlsx"style={{ display: 'none' }}/>
            <button onClick={() => fileRef.current ? fileRef.current.click() : ""} className="attachBtn btn">
              <img className="attach-icon" src={AttachIcon} alt="Send" />
            </button>
          </div>
        </div>
        
        
        
      </div>
    </>
  )
}

export default ChatBox;