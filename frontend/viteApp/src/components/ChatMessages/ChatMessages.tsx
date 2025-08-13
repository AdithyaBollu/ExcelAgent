import "./ChatMessages.css";
import ReactMarkdown from 'react-markdown';
import remarkGfm from "remark-gfm";

import download_file from "../../utils/file_helper";
import { useEffect, useRef } from "react";

interface Message {
    role: string;
    content: string;
    downloadUrl?: string;
    filename?: string;
}


type props = {
    messages: Message[];
    sentMessage?: boolean;
    generating?: boolean;
}

const ChatMessages: React.FC<props> = ({ messages, sentMessage, generating }) => {

    const messagesEndRef = useRef<HTMLDivElement>(null);
    const messagesContainerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        scrollToBottom();
    }, [messages, generating]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({
            behavior: "smooth",
            block: "end",
        })
    }

    const handleDownload = async (download_url: string, filename: string) => {
        try {
            await download_file(download_url, filename);
            console.log(`Downloaded: ${filename}`);
        }   
        catch(error) {
            console.log("UI Error: ", error);
        }
    }

    return (
        <>
        <div ref={messagesContainerRef} className={sentMessage ? "messages-full-container" : "messages-part-container"}>
            
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
                            {message.downloadUrl && message.filename && (
                                <div 
                                    className="download-btn"
                                    onClick={() => handleDownload(message.downloadUrl!, message.filename!)}
                                >
                                    Download File
                                </div>
                            )}
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

            <div ref={messagesEndRef} />
        </div>
        </>
    )
}

export default ChatMessages;