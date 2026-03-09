// Global variables
let video = null;
let canvas = null;
let currentMood = 'neutral';
let stream = null;

// Ambient Sound System
let ambientAudio = null;
let musicAudio = null;
let isAmbientPlaying = false;
let isMusicPlaying = false;
let ambientVolume = 0.3;
let musicVolume = 0.5;

// Mood-based ambient sounds (using free ambient sound URLs)
const ambientSounds = {
    'happy': 'https://cdn.pixabay.com/audio/2022/03/10/audio_4f8f803d1a.mp3', // Upbeat ambient
    'sad': 'https://cdn.pixabay.com/audio/2022/05/27/audio_1808fbf07a.mp3', // Calm rain
    'angry': 'https://cdn.pixabay.com/audio/2022/03/15/audio_c9aee0f2e7.mp3', // Tension relief
    'neutral': 'https://cdn.pixabay.com/audio/2022/03/10/audio_c8ec5738e1.mp3', // Peaceful ambient
    'surprise': 'https://cdn.pixabay.com/audio/2022/11/22/audio_6e5d0d6023.mp3', // Wonder sounds
    'fear': 'https://cdn.pixabay.com/audio/2022/05/27/audio_1808fbf07a.mp3', // Calming sounds
    'disgust': 'https://cdn.pixabay.com/audio/2022/03/10/audio_c8ec5738e1.mp3' // Neutral ambient
};

// Sample song data (BIBA or others can be added)
const songLibrary = {
    'biba': {
        title: 'BIBA',
        artists: 'Marshmello, Pritam Chakraborty, Shirley Setia, Pardeep Singh Sran, Dev Negi',
        album: 'BIBA',
        url: 'http://h.saavncdn.com/987/cd902d048c13e5ce6ca84cc409746a5d.mp3',
        image: 'https://c.saavncdn.com/987/BIBA-English-2019-20190201201359-500x500.jpg',
        duration: 175,
        year: 2019
    }
};

let currentSong = null;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    initializeAudioSystem();
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
    
    // Start ambient sound based on mood
    setTimeout(() => {
        playAmbientSound(currentMood);
    }, 1000);
    
    // Add initial greeting based on mood
    const greetings = {
        'happy': "Your emotional profile indicates positivity. I'm optimized to help enhance your productive state. How may I assist you?",
        'sad': "I've detected a subdued emotional state. I'm here to provide support and assistance. What can I help you with today?",
        'angry': "Your current emotional profile suggests elevated stress. Let's work together to address your concerns systematically.",
        'neutral': "System initialized. How can the AI platform assist you today?",
        'surprise': "I've detected heightened curiosity in your emotional profile. I'm ready to address your inquiries.",
        'fear': "Your emotional state indicates concern. I'm here to provide reliable support and information.",
        'disgust': "I'm here to assist you. Please share what's on your mind today."
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

// Show typing indicator with premium animation
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
                <p>
                    <span>AI is analyzing your message</span>
                    <span class="thinking-dots">
                        <span class="thinking-dot"></span>
                        <span class="thinking-dot"></span>
                        <span class="thinking-dot"></span>
                    </span>
                </p>
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

// =========================
// AMBIENT SOUND SYSTEM
// =========================

function initializeAudioSystem() {
    // Create audio elements
    ambientAudio = new Audio();
    ambientAudio.loop = true;
    ambientAudio.volume = ambientVolume;
    
    musicAudio = new Audio();
    musicAudio.loop = false;
    musicAudio.volume = musicVolume;
    
    // Set up event listeners for audio controls
    setupAudioControls();
    
    console.log('Audio system initialized');
}

function setupAudioControls() {
    const ambientToggle = document.getElementById('ambientToggle');
    const musicToggle = document.getElementById('musicToggle');
    const ambientVolumeSlider = document.getElementById('ambientVolume');
    const musicVolumeSlider = document.getElementById('musicVolume');
    
    if (ambientToggle) {
        ambientToggle.addEventListener('click', toggleAmbientSound);
    }
    
    if (musicToggle) {
        musicToggle.addEventListener('click', toggleMusic);
    }
    
    if (ambientVolumeSlider) {
        ambientVolumeSlider.addEventListener('input', (e) => {
            ambientVolume = e.target.value / 100;
            if (ambientAudio) {
                ambientAudio.volume = ambientVolume;
            }
        });
    }
    
    if (musicVolumeSlider) {
        musicVolumeSlider.addEventListener('input', (e) => {
            musicVolume = e.target.value / 100;
            if (musicAudio) {
                musicAudio.volume = musicVolume;
            }
        });
    }
    
    // Music ended event
    if (musicAudio) {
        musicAudio.addEventListener('ended', () => {
            isMusicPlaying = false;
            updateMusicControls();
        });
    }
}

function toggleAmbientSound() {
    if (isAmbientPlaying) {
        stopAmbientSound();
    } else {
        playAmbientSound(currentMood);
    }
}

function playAmbientSound(mood) {
    if (!ambientAudio) return;
    
    const soundUrl = ambientSounds[mood] || ambientSounds['neutral'];
    
    // Only change sound if it's different
    if (ambientAudio.src !== soundUrl) {
        ambientAudio.src = soundUrl;
    }
    
    ambientAudio.play()
        .then(() => {
            isAmbientPlaying = true;
            updateAmbientControls();
            console.log(`Playing ${mood} ambient sound`);
        })
        .catch(error => {
            console.error('Error playing ambient sound:', error);
            showNotification('Unable to play ambient sound. Click to enable audio.', 'warning');
        });
}

function stopAmbientSound() {
    if (ambientAudio) {
        ambientAudio.pause();
        isAmbientPlaying = false;
        updateAmbientControls();
    }
}

function changeAmbientSound(mood) {
    if (isAmbientPlaying) {
        // Fade out current, change, fade in new
        fadeOut(ambientAudio, () => {
            playAmbientSound(mood);
        });
    }
}

function toggleMusic() {
    if (isMusicPlaying) {
        stopMusic();
    } else {
        // Play default song (BIBA)
        playMusic('biba');
    }
}

function playMusic(songId) {
    const song = songLibrary[songId];
    if (!song || !musicAudio) return;
    
    currentSong = song;
    musicAudio.src = song.url;
    
    musicAudio.play()
        .then(() => {
            isMusicPlaying = true;
            updateMusicControls();
            updateNowPlaying(song);
            console.log(`Playing: ${song.title} by ${song.artists}`);
            
            // Show notification
            showMusicNotification(song);
        })
        .catch(error => {
            console.error('Error playing music:', error);
            showNotification('Unable to play music. Click to enable audio.', 'warning');
        });
}

function stopMusic() {
    if (musicAudio) {
        musicAudio.pause();
        musicAudio.currentTime = 0;
        isMusicPlaying = false;
        currentSong = null;
        updateMusicControls();
        updateNowPlaying(null);
    }
}

function updateAmbientControls() {
    const ambientToggle = document.getElementById('ambientToggle');
    const ambientIcon = document.getElementById('ambientIcon');
    
    if (ambientToggle) {
        if (isAmbientPlaying) {
            ambientToggle.classList.add('active');
            if (ambientIcon) ambientIcon.className = 'fas fa-volume-up';
        } else {
            ambientToggle.classList.remove('active');
            if (ambientIcon) ambientIcon.className = 'fas fa-volume-mute';
        }
    }
}

function updateMusicControls() {
    const musicToggle = document.getElementById('musicToggle');
    const musicIcon = document.getElementById('musicIcon');
    
    if (musicToggle) {
        if (isMusicPlaying) {
            musicToggle.classList.add('active');
            if (musicIcon) musicIcon.className = 'fas fa-pause';
        } else {
            musicToggle.classList.remove('active');
            if (musicIcon) musicIcon.className = 'fas fa-play';
        }
    }
}

function updateNowPlaying(song) {
    const nowPlayingDiv = document.getElementById('nowPlaying');
    
    if (!nowPlayingDiv) return;
    
    if (song) {
        nowPlayingDiv.innerHTML = `
            <div class="song-info">
                <img src="${song.image}" alt="${song.title}" class="song-cover">
                <div class="song-details">
                    <div class="song-title">${song.title}</div>
                    <div class="song-artist">${song.artists}</div>
                </div>
            </div>
        `;
        nowPlayingDiv.style.display = 'flex';
    } else {
        nowPlayingDiv.style.display = 'none';
    }
}

function showMusicNotification(song) {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;
    
    const notification = document.createElement('div');
    notification.className = 'music-notification';
    notification.innerHTML = `
        <i class="fas fa-music"></i>
        <span>Now playing: <strong>${song.title}</strong> by ${song.artists}</span>
    `;
    
    chatMessages.appendChild(notification);
    scrollToBottom();
    
    // Remove notification after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Fade out audio
function fadeOut(audio, callback) {
    const fadeInterval = setInterval(() => {
        if (audio.volume > 0.1) {
            audio.volume -= 0.1;
        } else {
            clearInterval(fadeInterval);
            audio.pause();
            audio.volume = ambientVolume; // Reset volume
            if (callback) callback();
        }
    }, 100);
}

// Update mood indicator and change ambient sound
function updateMoodWithAmbient(mood) {
    updateMoodIndicator(mood);
    if (isAmbientPlaying) {
        changeAmbientSound(mood);
    }
}

