
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
      {'role': 'user', 'content': 'Folsom'}, {'role': 'assistant', 'content': 'Here is the current weather for Folsom, California:\n\n- **Temperature**: 36.4°C (97.5°F)\n- **Conditions**: Sunny\n- **Wind Speed**: 5.4 mph (8.6 kph) from the WSW\n- **Humidity**: 25%\n- **Pressure**: 1012 mb (29.89 in)\n- **Visibility**: 16 km (9 miles)\n- **Heat Index**: 40.3°C (104.6°F)\n- **UV Index**: 8.1 (High)\n\nIf you need more information or updates, feel free to ask!'},
      {'role': 'user', 'content': 'How much protein in chicken vs mutton, make a table'}, 
      {'role': 'assistant', 'content': "Here's a comparison table of protein content in chicken and mutton:\n\n| Food          | Serving Size (g) | Protein (g) | Total Fat (g) | Saturated Fat (g) | Calories |\n|---------------|------------------|-------------|----------------|-------------------|---------|\n| Chicken Breast| 100              | 31.0        | 3.5            | 1.0               | 166.2   |\n| Mutton        | 100              | 24.4        | 21.3           | 8.9               | 289.6   |\n\nIf you have any more questions or need further information, feel free to ask!"}
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