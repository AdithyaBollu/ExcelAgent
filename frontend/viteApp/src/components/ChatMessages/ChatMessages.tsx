import "./ChatMessages.css";
import ReactMarkdown from 'react-markdown';

interface Message {
    role: string;
    content: string;
}


type props = {
    messages: Message[];
}

const ChatMessages: React.FC<props> = ({ messages }) => {


    return (
        <>
        <div className="messages-container">
            
            {messages.map((message) => {
                if (message.role === 'user') {
                    return (
                        <div className="message user-message" key={message.content}>
                            <div className="message-content">{message.content}</div>
                        </div>
                    );
                } else if (message.role === 'assistant') {
                    return (
                        <div className="message assistant-message" key={message.content}>
                            <div className="message-content">
                                <ReactMarkdown>{message.content}</ReactMarkdown>
                            </div>
                        </div>
                    );
                }
            })}
        </div>
        </>
    )
}

export default ChatMessages;