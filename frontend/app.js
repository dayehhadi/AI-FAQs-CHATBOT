document.getElementById('chat-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const userInput = document.getElementById('user-input').value.trim();
    if (userInput === "") return; // Prevent sending empty messages

    appendMessage('You', userInput, 'user-msg');
    document.getElementById('user-input').value = '';
    scrollToBottom();

    // Optional: Add a loading indicator
    appendMessage('Bot', 'Typing...', 'bot-msg typing');
    scrollToBottom();

    try {
        // Send the message to the backend
        const response = await fetch('http://localhost:5000/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userInput })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        // Remove the loading indicator
        removeLastMessage('typing');

        // Append the bot's response
        appendMessage('Bot', data.response, 'bot-msg');
    } catch (error) {
        // Remove the loading indicator
        removeLastMessage('typing');

        // Display error message
        appendMessage('Bot', 'Sorry, something went wrong. Please try again later.', 'bot-msg');
        console.error('Error:', error);
    }

    scrollToBottom();
});

// Function to append messages to the chat box
function appendMessage(sender, message, className) {
    const chatBox = document.getElementById('chat-box');
    const msgDiv = document.createElement('div');
    msgDiv.className = className;
    msgDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(msgDiv);
}

// Function to remove the last message based on className
function removeLastMessage(className) {
    const chatBox = document.getElementById('chat-box');
    const messages = chatBox.getElementsByClassName(className);
    if (messages.length > 0) {
        chatBox.removeChild(messages[messages.length - 1]);
    }
}

// Function to scroll the chat box to the bottom
function scrollToBottom() {
    const chatBox = document.getElementById('chat-box');
    chatBox.scrollTop = chatBox.scrollHeight;
}
