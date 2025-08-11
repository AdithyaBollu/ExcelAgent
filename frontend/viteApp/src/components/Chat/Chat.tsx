
import { useState } from "react";
import ChatBox from "../Chatbox/ChatBox.tsx";
import ChatMessages from "../ChatMessages/ChatMessages.tsx";
import './Chat.css';

function Chat() {
  const [messages, setMessages] = useState([
    {'role': 'user', 'content': 'Hello'}, 
      {'role': 'assistant', 'content': 'How can I assist you today? If you have any questions about nutrition, dietary plans, or need information on food macros, feel free to ask!'}, 
      {'role': 'user', 'content': 'Tell me the weather'}, 
      {'role': 'assistant', 'content': 'Could you please specify the city or location for which you would like to know the weather?'}, 
      {'role': 'user', 'content': 'Folsom'}, {'role': 'assistant', 'content': 'Here is the current weather for Folsom, California:\n\n- **Temperature**: 36.4°C (97.5°F)\n- **Conditions**: Sunny\n- **Wind Speed**: 5.4 mph (8.6 kph) from the WSW\n- **Humidity**: 25%\n- **Pressure**: 1012 mb (29.89 in)\n- **Visibility**: 16 km (9 miles)\n- **Heat Index**: 40.3°C (104.6°F)\n- **UV Index**: 8.1 (High)\n\nIf you need more information or updates, feel free to ask!'}
    
    ])

  return (
    <>
      <div className="chat-container">
        
        <ChatMessages messages={messages}/>
        <ChatBox setMessages={setMessages}/>
      </div>
    </>
  )
}

export default Chat;