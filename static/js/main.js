// Global variables
let video = null;
let canvas = null;
let currentMood = 'neutral';
let stream = null;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    // Get DOM elements
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    
    // Mood detection buttons
    const startMoodBtn = document.getElementById('startMoodBtn');
    const captureMoodBtn = document.getElementById('captureMoodBtn');
    const skipMoodBtn = document.getElementById('skipMoodBtn');
    
    // Chat elements
    const sendBtn = document.getElementById('sendBtn');
    const messageInput = document.getElementById('messageInput');
    
    // Modal and stats
    const statsBtn = document.getElementById('statsBtn');
    const closeStatsBtn = document.getElementById('closeStatsBtn');
    const resetBtn = document.getElementById('resetBtn');
    
    // Event listeners
    startMoodBtn.addEventListener('click', startCamera);
    captureMoodBtn.addEventListener('click', captureMood);
    skipMoodBtn.addEventListener('click', skipMoodDetection);
    sendBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    statsBtn.addEventListener('click', showStats);
    closeStatsBtn.addEventListener('click', closeStats);
    resetBtn.addEventListener('click', resetSession);
    
    // Update time for initial message
    updateMessageTimes();
}

// Start camera for mood detection
async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: 'user' } 
        });
        
        video.srcObject = stream;
        
        document.getElementById('videoContainer').style.display = 'block';
        document.getElementById('startMoodBtn').style.display = 'none';
        document.getElementById('captureMoodBtn').style.display = 'block';
        
        showNotification('Camera started! Position your face and click Capture', 'info');
    } catch (error) {
        console.error('Camera error:', error);
        showNotification('Unable to access camera. You can skip and start chatting.', 'error');
    }
}

// Capture and analyze mood
async function captureMood() {
    showLoading(true);
    
    try {
        // Set canvas dimensions to match video
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        // Draw current video frame to canvas
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);
        
        // Get image data
        const imageData = canvas.toDataURL('image/jpeg', 0.8);
        
        // Send to server for mood detection
        const response = await fetch('/detect_mood', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentMood = data.mood;
            displayMoodResult(data.mood, data.message);
            
            // Stop camera
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }
            
            // Show chat interface after 2 seconds
            setTimeout(() => {
                showChatInterface();
            }, 2000);
        } else {
            showNotification('Mood detection failed. Starting with neutral mood.', 'warning');
            setTimeout(() => {
                showChatInterface();
            }, 1500);
        }
    } catch (error) {
        console.error('Mood detection error:', error);
        showNotification('Error detecting mood. Starting with neutral mood.', 'error');
        setTimeout(() => {
            showChatInterface();
        }, 1500);
    } finally {
        showLoading(false);
    }
}

// Display mood result
function displayMoodResult(mood, message) {
    const moodResult = document.getElementById('moodResult');
    const moodIcon = document.getElementById('moodIcon');
    const moodText = document.getElementById('moodText');
    const moodMessage = document.getElementById('moodMessage');
    
    const moodEmojis = {
        'happy': '😊',
        'sad': '😢',
        'angry': '😠',
        'neutral': '😐',
        'surprise': '😮',
        'fear': '😨',
        'disgust': '🤢'
    };
    
    moodIcon.textContent = moodEmojis[mood] || '😐';
    moodText.textContent = mood.charAt(0).toUpperCase() + mood.slice(1);
    moodMessage.textContent = message;
    
    document.getElementById('videoContainer').style.display = 'none';
    document.getElementById('captureMoodBtn').style.display = 'none';
    moodResult.style.display = 'block';
}

// Skip mood detection
function skipMoodDetection() {
    currentMood = 'neutral';
    showChatInterface();
}

// Show chat interface
function showChatInterface() {
    document.getElementById('moodPanel').style.display = 'none';
    document.getElementById('chatInterface').style.display = 'grid';
    
    // Update mood indicator
    updateMoodIndicator(currentMood);
    
    // Add initial greeting based on mood
    const greetings = {
        'happy': "I can see you're in a great mood! How can I make your day even better?",
        'sad': "I'm here for you. Would you like to talk about what's bothering you?",
        'angry': "I understand you might be frustrated. Let's work through this together.",
        'neutral': "How can I assist you today?",
        'surprise': "Something unexpected? I'm all ears!",
        'fear': "It's okay to feel worried. I'm here to help.",
        'disgust': "I'm listening. Tell me what's on your mind."
    };
    
    if (currentMood !== 'neutral') {
        addBotMessage(greetings[currentMood] || greetings['neutral']);
    }
    
    // Focus on input
    document.getElementById('messageInput').focus();
}

// Update mood indicator
function updateMoodIndicator(mood) {
    const moodLabel = document.getElementById('moodLabel');
    const moodIndicator = document.getElementById('currentMood');
    
    moodLabel.textContent = mood.charAt(0).toUpperCase() + mood.slice(1);
    
    const moodIcons = {
        'happy': 'fa-smile',
        'sad': 'fa-sad-tear',
        'angry': 'fa-angry',
        'neutral': 'fa-meh',
        'surprise': 'fa-surprise',
        'fear': 'fa-frown',
        'disgust': 'fa-grimace'
    };
    
    const icon = moodIndicator.querySelector('i');
    icon.className = `fas ${moodIcons[mood] || 'fa-smile'}`;
}

// Send message
async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addUserMessage(message);
    messageInput.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        // Send to server
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                message: message,
                mood: currentMood 
            })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        if (data.success) {
            addBotMessage(data.response);
        } else {
            addBotMessage("I'm sorry, I encountered an error. Please try again.");
        }
    } catch (error) {
        console.error('Chat error:', error);
        removeTypingIndicator();
        addBotMessage("I'm having trouble connecting. Please try again.");
    }
}

// Add user message to chat
function addUserMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = createMessageElement(message, 'user');
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Add bot message to chat
function addBotMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = createMessageElement(message, 'bot');
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Create message element
function createMessageElement(message, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = type === 'bot' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.innerHTML = `<p>${escapeHtml(message)}</p>`;
    
    const time = document.createElement('span');
    time.className = 'message-time';
    time.textContent = getCurrentTime();
    
    content.appendChild(bubble);
    content.appendChild(time);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    return messageDiv;
}

// Show typing indicator
function showTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing-indicator';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="message-bubble">
                <p>Thinking...</p>
            </div>
        </div>
    `;
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
}

// Remove typing indicator
function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

// Scroll chat to bottom
function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Show statistics modal
async function showStats() {
    try {
        const response = await fetch('/stats');
        const stats = await response.json();
        
        document.getElementById('totalConversations').textContent = stats.total_conversations;
        document.getElementById('topicsLearned').textContent = stats.topics_learned;
        document.getElementById('userName').textContent = stats.user_name;
        
        document.getElementById('statsModal').classList.add('active');
    } catch (error) {
        console.error('Stats error:', error);
        showNotification('Unable to load statistics', 'error');
    }
}

// Close statistics modal
function closeStats() {
    document.getElementById('statsModal').classList.remove('active');
}

// Reset session
async function resetSession() {
    if (!confirm('Are you sure you want to start a new session? This will reset the mood detection.')) {
        return;
    }
    
    try {
        await fetch('/reset', { method: 'POST' });
        location.reload();
    } catch (error) {
        console.error('Reset error:', error);
        showNotification('Unable to reset session', 'error');
    }
}

// Show/hide loading overlay
function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    if (show) {
        overlay.classList.add('active');
    } else {
        overlay.classList.remove('active');
    }
}

// Show notification
function showNotification(message, type = 'info') {
    // Simple alert for now - could be enhanced with custom notification UI
    console.log(`[${type.toUpperCase()}] ${message}`);
}

// Get current time
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

// Update message times
function updateMessageTimes() {
    const times = document.querySelectorAll('.message-time');
    times.forEach(time => {
        if (!time.textContent) {
            time.textContent = getCurrentTime();
        }
    });
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Close modal on outside click
window.addEventListener('click', (e) => {
    const modal = document.getElementById('statsModal');
    if (e.target === modal) {
        closeStats();
    }
});
