import { useState, useEffect, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { chatAPI } from '../services/api';
import styles from './Chat.module.css';

export default function Chat() {
  const { user } = useAuth();
  const [searchParams] = useSearchParams();
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [sendingMessage, setSendingMessage] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    const fetchConversations = async () => {
      try {
        setLoading(true);
        const data = await chatAPI.getConversations();
        setConversations(data);

        // Auto-select conversation from URL parameter
        const conversationId = searchParams.get('conversation');
        if (conversationId && data.length > 0) {
          const conv = data.find(c => c.id === parseInt(conversationId));
          if (conv) {
            setSelectedConversation(conv);
          }
        } else if (data.length > 0) {
          setSelectedConversation(data[0]);
        }
      } catch (err) {
        console.error('Error fetching conversations:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchConversations();
  }, [searchParams]);

  useEffect(() => {
    const fetchMessages = async () => {
      if (!selectedConversation) return;

      try {
        const data = await chatAPI.getMessages(selectedConversation.id);
        setMessages(data);
        setTimeout(scrollToBottom, 100);
      } catch (err) {
        console.error('Error fetching messages:', err);
      }
    };

    fetchMessages();
    // Poll for new messages every 3 seconds
    const interval = setInterval(fetchMessages, 3000);
    return () => clearInterval(interval);
  }, [selectedConversation]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !selectedConversation) return;

    setSendingMessage(true);
    try {
      const message = await chatAPI.sendMessage(selectedConversation.id, newMessage);
      setMessages([...messages, message]);
      setNewMessage('');
      setTimeout(scrollToBottom, 100);
    } catch (err) {
      console.error('Error sending message:', err);
      alert('Failed to send message');
    } finally {
      setSendingMessage(false);
    }
  };

  const getOtherParticipant = (conversation) => {
    if (!user) return null;
    return conversation.participant1_id === user.id
      ? conversation.participant2
      : conversation.participant1;
  };

  const formatTime = (dateStr) => {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  if (loading) {
    return <div className={styles.loading}>Loading conversations...</div>;
  }

  if (conversations.length === 0) {
    return (
      <div className={styles.emptyState}>
        <h2>No conversations yet</h2>
        <p>Start a conversation by visiting a user's profile and clicking "Send Message"</p>
      </div>
    );
  }

  return (
    <div className={styles.chatPage}>
      <div className={styles.container}>
        {/* Conversations List */}
        <aside className={styles.sidebar}>
          <h2 className={styles.sidebarTitle}>Messages</h2>
          <div className={styles.conversationsList}>
            {conversations.map((conv) => {
              const otherUser = getOtherParticipant(conv);
              if (!otherUser) return null;

              return (
                <div
                  key={conv.id}
                  className={`${styles.conversationItem} ${
                    selectedConversation?.id === conv.id ? styles.active : ''
                  }`}
                  onClick={() => setSelectedConversation(conv)}
                >
                  <img
                    src={otherUser.avatar || 'https://i.pravatar.cc/100'}
                    alt={otherUser.name}
                    className={styles.conversationAvatar}
                  />
                  <div className={styles.conversationInfo}>
                    <div className={styles.conversationName}>{otherUser.name}</div>
                    <div className={styles.conversationPreview}>
                      {conv.messages && conv.messages.length > 0
                        ? conv.messages[conv.messages.length - 1].content.substring(0, 40)
                        : 'No messages yet'}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </aside>

        {/* Chat Window */}
        <main className={styles.chatWindow}>
          {selectedConversation ? (
            <>
              <div className={styles.chatHeader}>
                <img
                  src={getOtherParticipant(selectedConversation)?.avatar || 'https://i.pravatar.cc/100'}
                  alt={getOtherParticipant(selectedConversation)?.name}
                  className={styles.chatHeaderAvatar}
                />
                <h3 className={styles.chatHeaderName}>
                  {getOtherParticipant(selectedConversation)?.name}
                </h3>
              </div>

              <div className={styles.messagesContainer}>
                {messages.length === 0 ? (
                  <div className={styles.noMessages}>
                    <p>No messages yet. Start the conversation!</p>
                  </div>
                ) : (
                  messages.map((message) => (
                    <div
                      key={message.id}
                      className={`${styles.message} ${
                        message.sender_id === user?.id ? styles.sent : styles.received
                      }`}
                    >
                      <div className={styles.messageContent}>{message.content}</div>
                      <div className={styles.messageTime}>{formatTime(message.sent_at)}</div>
                    </div>
                  ))
                )}
                <div ref={messagesEndRef} />
              </div>

              <form onSubmit={handleSendMessage} className={styles.messageForm}>
                <input
                  type="text"
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  placeholder="Type a message..."
                  className={styles.messageInput}
                  disabled={sendingMessage}
                />
                <button
                  type="submit"
                  className={styles.sendButton}
                  disabled={sendingMessage || !newMessage.trim()}
                >
                  {sendingMessage ? 'Sending...' : 'Send'}
                </button>
              </form>
            </>
          ) : (
            <div className={styles.noConversationSelected}>
              <p>Select a conversation to start messaging</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
