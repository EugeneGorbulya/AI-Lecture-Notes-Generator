import React, { useState, useEffect } from "react";
import { getUserId, getToken, saveUserId } from "../utils/auth";
import "../styles/UserDashboard.css";

function UserDashboard() {
  const [chats, setChats] = useState([]);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [file, setFile] = useState(null);
  const [newChatName, setNewChatName] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedChat, setSelectedChat] = useState(null);

  useEffect(() => {
    const fetchUserId = async () => {
      try {
        const token = getToken();
        if (!token) {
          console.error("No access token found");
          return;
        }

        const response = await fetch("http://127.0.0.1:8000/api/users/me", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          saveUserId(data.id);
        } else {
          console.error("Failed to fetch user data");
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    };

    const fetchChats = async () => {
      const token = getToken();
      if (!token) {
        console.error("No access token found");
        return;
      }

      try {
        const response = await fetch("http://127.0.0.1:8000/api/chats", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (response.ok) {
          const data = await response.json();
          setChats(data);
        } else {
          console.error("Failed to fetch chats");
        }
      } catch (error) {
        console.error("Error fetching chats:", error);
      }
    };

    fetchUserId();
    fetchChats();
  }, []);

  const fetchMessages = async (chatId) => {
    const token = getToken();
    if (!token) {
      console.error("No access token found");
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/message/${chatId}/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (response.ok) {
        const data = await response.json();
        setMessages(data);
      } else {
        console.error("Failed to fetch messages");
      }
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  };

  const handleSelectChat = (chat) => {
    setSelectedChat(chat);
    fetchMessages(chat.id);
  };

  const handleCreateChat = async () => {
    if (!newChatName.trim()) {
      alert("Chat name cannot be empty!");
      return;
    }

    const userId = getUserId();

    if (!userId) {
      alert("User not logged in. Please log in to create a chat.");
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/chats/?user_id=${userId}&name=${newChatName}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        }
      );

      if (response.ok) {
        const newChat = await response.json();
        setChats([...chats, newChat]);
        setNewChatName("");
        setIsModalOpen(false);
      } else {
        const errorData = await response.json();
        console.error("Error creating chat:", errorData);
        alert(`Error creating chat: ${errorData.detail || "Unknown error"}`);
      }
    } catch (error) {
      console.error("Network error while creating chat:", error);
      alert(`An unexpected error occurred: ${error.message}`);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleFileDownload = (fileUrl, fileName) => {
    const apiUrl = "http://127.0.0.1:8000/api/message/static/"; // Ваш базовый путь
    const fullUrl = `${apiUrl}${fileName}`;

    const anchor = document.createElement("a");
    anchor.href = fullUrl;
    anchor.download = fileName;
    document.body.appendChild(anchor);
    anchor.click();
    document.body.removeChild(anchor);
};




  const handleFileUpload = async (e) => {
    if (!selectedChat) {
      alert("Please select a chat before uploading a file.");
      return;
    }

    const token = getToken();
    if (!token) {
      console.error("No access token found");
      return;
    }

    const uploadedFile = e.target.files[0];
    if (!uploadedFile) return;

    const formData = new FormData();
    formData.append("file", uploadedFile); // Загружаемый файл
    formData.append("type", "VIDEO"); // Тип сообщения

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/message/${selectedChat.id}/file`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      );

      if (response.ok) {
        const newMessage = await response.json();
        setMessages([...messages, newMessage]); // Добавляем новое сообщение в список
      } else {
        const errorData = await response.json();
        console.error("Error uploading file:", errorData);
        alert(`Failed to upload file: ${errorData.detail || "Unknown error"}`);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      alert(`An unexpected error occurred: ${error.message}`);
    } finally {
      e.target.value = null; // Сброс input-файла
    }
  };


  const handleSendMessage = async () => {
    if (!input.trim() || !selectedChat) {
      alert("Please select a chat and type a message.");
      return;
    }

    const token = getToken();
    if (!token) {
      console.error("No access token found");
      return;
    }

    try {
      const payload = {
        type: "TEXT", // Тип сообщения
        content: input, // Содержимое сообщения
        chat_id: selectedChat.id, // ID чата
      };

      const response = await fetch(
        `http://127.0.0.1:8000/api/message/${selectedChat.id}/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(payload),
        }
      );

      if (response.ok) {
        const newMessage = await response.json();
        setMessages([...messages, newMessage]);
        setInput("");
      } else {
        console.error("Failed to send message");
      }
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        <h2>Chat History</h2>
        <ul>
          {chats.map((chat) => (
            <li
              key={chat.id}
              onClick={() => handleSelectChat(chat)}
              className={`chat-item ${
                selectedChat?.id === chat.id ? "selected" : ""
              }`}
            >
              {chat.name}
            </li>
          ))}
        </ul>
        <button className="new-chat-btn" onClick={() => setIsModalOpen(true)}>
          + New Chat
        </button>
      </aside>

      <main className="chat-container">
        <header className="chat-header">
          <h2>{selectedChat ? selectedChat.name : "Select a Chat"}</h2>
        </header>
        <div className="chat-messages">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.sender === "user" ? "user" : "bot"}`}
            >
              {message.url ? (
                <span
                  className="clickable-file"
                  onClick={() => handleFileDownload(message.url, message.content)}
                >
                  {message.content}
                </span>
              ) : (
                message.content
              )}
            </div>
          ))}
        </div>
        <footer
          className={`chat-input ${!selectedChat ? "disabled-footer" : ""}`}
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            disabled={!selectedChat}
            onKeyDown={handleKeyDown}
          />
          <input
            type="file"
            style={{ display: "none" }}
            id="file-upload"
            onChange={handleFileUpload}
            disabled={!selectedChat}
          />
          <label
            htmlFor="file-upload"
            className={`upload-btn ${
              !selectedChat ? "disabled-button" : ""
            }`}
          >
            Upload File
          </label>
          <button
            onClick={handleSendMessage}
            disabled={!selectedChat}
            className={`send-btn ${!selectedChat ? "disabled-button" : ""}`}
          >
            Send
          </button>
        </footer>
      </main>

      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Create New Chat</h3>
            <input
              type="text"
              value={newChatName}
              onChange={(e) => setNewChatName(e.target.value)}
              placeholder="Enter chat name"
            />
            <div className="modal-buttons">
              <button onClick={handleCreateChat}>Create</button>
              <button onClick={() => setIsModalOpen(false)}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default UserDashboard;
