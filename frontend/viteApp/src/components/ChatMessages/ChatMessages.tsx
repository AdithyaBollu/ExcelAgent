import "./ChatMessages.css";
import ReactMarkdown from 'react-markdown';
import remarkGfm from "remark-gfm";

interface Message {
    role: string;
    content: string;
}


type props = {
    messages: Message[];
    sentMessage?: boolean;
    generating?: boolean;
}

const ChatMessages: React.FC<props> = ({ messages, sentMessage, generating }) => {


    return (
        <>
        <div className={sentMessage ? "messages-full-container" : "messages-part-container"}>
            
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
                                <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
                            </div>
                        </div>
                    );
                }
            })}
            { generating && <div className="message typing-indicator loader">
                <span></span>
                <span></span>
                <span></span>
                {/* <span>.</span> */}
            </div> }
        </div>
        </>
    )
}

export default ChatMessages;