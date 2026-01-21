# CoconuT-Ai 🥥🤖
**A Self-Learning AI Chatbot with Mood Detection & Dynamic Responses**

An intelligent AI chatbot that detects your mood through facial recognition and provides personalized, empathetic responses. The AI learns from every conversation, building a knowledge base to better understand and assist you over time.

## ✨ Key Features

### 🎭 Mood Detection
- Real-time facial emotion recognition using DeepFace
- Detects 7 emotions: happy, sad, angry, surprise, fear, disgust, neutral
- Camera-based mood analysis before each session

### 🧠 Self-Learning AI System
- **Automatic Learning**: Learns patterns from every conversation
- **Persistent Memory**: Saves knowledge between sessions
- **Topic Recognition**: Identifies and remembers topics you discuss
- **Personalization**: Remembers your name and preferences
- **Word Associations**: Builds connections between words and moods
- **Conversation History**: Tracks all interactions with timestamps

### 💬 Dynamic Response Generation
- Context-aware responses based on current mood
- Personalized greetings using learned user information
- Intelligent question handling
- Sentiment analysis of user input
- Natural conversation flow with varied responses

### 📊 Learning Analytics
- View conversation statistics
- Track topics learned
- Monitor AI's learning progress
- See mood encounter patterns

### 🎨 Enhanced User Interface
- Modern, colorful design
- Scrollable chat window
- Color-coded messages (user vs AI)
- Real-time text-to-speech responses
- Enter key support for quick messaging
- Stats viewer for learning progress

## 🚀 How It Works

1. **Mood Detection**: The AI uses your camera to analyze your facial expression
2. **Personalized Greeting**: Based on detected mood, provides an appropriate welcome
3. **Dynamic Conversation**: Responds intelligently to your inputs
4. **Continuous Learning**: Every message helps the AI learn more about you
5. **Knowledge Persistence**: All learned information is saved for future sessions

## 📦 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/CoconuT-Ai.git
cd CoconuT-Ai
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python CoconutAi.py
```

## 🔧 Requirements

- Python 3.8+
- Webcam for mood detection
- Windows/Mac/Linux OS

**Dependencies**:
- opencv-python: For camera access and image processing
- deepface: For facial emotion recognition
- pyttsx3: For text-to-speech functionality
- Pillow: For image handling
- tensorflow: Backend for DeepFace

## 📖 Usage Guide

1. **Start the Application**: Run the Python script
2. **Click "Start Mood Detection"**: Allow camera access
3. **Let AI Detect Your Mood**: Position your face in view
4. **Start Chatting**: Type messages and press Enter or click Send
5. **View Stats**: Click "View Stats" to see learning progress
6. **Exit**: Type "exit", "quit", or "bye" to end the session

## 🤖 AI Learning Capabilities

The AI learns and improves through:

- **Pattern Recognition**: Identifies common conversation patterns
- **Topic Extraction**: Recognizes subjects like work, family, health, hobbies
- **Mood Correlation**: Associates words with emotional states
- **User Profiling**: Builds a profile of your preferences
- **Response Optimization**: Improves response quality over time

### Data Storage

The AI stores learned data in:
- `ai_knowledge.pkl`: Main knowledge base (patterns, responses, topics)
- `user_preferences.json`: Your personal information and preferences

## 🎯 Features in Detail

### Mood-Based Responses
- **Happy**: Enthusiastic and energetic responses
- **Sad**: Empathetic and supportive messages
- **Angry**: Calm and understanding approach
- **Neutral**: Balanced, helpful responses
- **Fear**: Reassuring and comforting words
- **Surprise**: Curious and engaged reactions
- **Disgust**: Understanding and supportive dialogue

### Dynamic Response Types
- Greeting recognition
- Question answering
- Sentiment-aware replies
- Context-based responses
- Personalized messages with your name
- Topic-referenced conversations

## 🛠️ Customization

You can customize the AI by:
- Editing default mood responses in `get_default_mood_responses()`
- Adding new topic keywords in `extract_topics()`
- Modifying response generation logic in `generate_response()`
- Adjusting learning frequency in `learn_from_input()`

## 🔒 Privacy

- All data is stored locally on your machine
- No information is sent to external servers
- Camera is only used for mood detection
- You can delete `ai_knowledge.pkl` and `user_preferences.json` anytime to reset

## 🐛 Troubleshooting

**Camera not working?**
- Ensure your webcam is connected
- Check camera permissions in system settings
- Close other applications using the camera

**AI not learning?**
- Check if pickle files are being created
- Ensure write permissions in the directory
- Verify enough disk space available

**Dependencies issues?**
- Use Python 3.8 or higher
- Try: `pip install --upgrade pip`
- Install dependencies one by one if batch install fails

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created with ❤️ by [Your Name]

## 🙏 Acknowledgments

- DeepFace for emotion recognition
- OpenCV for camera handling
- The Python community

---

**Note**: This AI is designed to be a supportive companion. It learns from interactions to provide better assistance, but it's not a replacement for professional mental health support.
