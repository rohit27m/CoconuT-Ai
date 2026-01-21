# 🚀 Quick Setup Guide for CoconuT-Ai

## Step-by-Step Installation

### 1. Prerequisites
- Python 3.8 or higher installed
- Webcam connected to your computer
- Internet connection (for initial package download)

### 2. Install Python Packages

Open your terminal/command prompt in the project directory and run:

```bash
pip install opencv-python deepface pyttsx3 Pillow tensorflow
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### 3. First Run

```bash
python CoconutAi.py
```

### 4. Using the Application

1. **Click "Start Mood Detection"** - The camera will activate
2. **Look at the camera** - Let the AI detect your facial expression
3. **Start chatting** - Type your message and press Enter
4. **Teach the AI** - Tell it your name, interests, and feelings
5. **View progress** - Click "View Stats" to see what the AI has learned

## 🎯 First Time Tips

### Introduce Yourself
Start by saying: "Hi, my name is [Your Name]"
- The AI will remember your name for future conversations

### Test Different Moods
- Try the app when you're happy, sad, or neutral
- See how the AI adapts its responses

### Ask Questions
- "How are you?"
- "What can you help me with?"
- "Can you tell me about yourself?"

### Share Your Day
Tell the AI about:
- Your work or studies
- Your hobbies
- Your feelings
- Your experiences

## 📁 Generated Files

After first use, you'll see these files:
- `ai_knowledge.pkl` - The AI's learned knowledge
- `user_preferences.json` - Your personal preferences

**Note**: Don't delete these files if you want the AI to remember previous conversations!

## 🔧 Troubleshooting

### Camera Issues
```python
# If camera doesn't work, check:
1. Is the webcam connected?
2. Are other apps using the camera?
3. Does your OS allow camera access for Python?
```

### Installation Errors
```bash
# If pip install fails, try:
pip install --upgrade pip
pip install --user opencv-python deepface pyttsx3 Pillow tensorflow
```

### Module Not Found Error
```bash
# Make sure you're in the right directory:
cd CoconuT-Ai
python CoconutAi.py
```

## 💡 Pro Tips

1. **Be Natural**: Talk to the AI like a friend
2. **Be Specific**: Mention specific topics for better learning
3. **Give Feedback**: The more you chat, the smarter it gets
4. **Regular Use**: Use it daily to build a better knowledge base
5. **Reset if Needed**: Delete .pkl and .json files to start fresh

## 🎓 Learning Progress

The AI learns from:
- ✅ Every message you send
- ✅ Topics you mention (work, family, hobbies, etc.)
- ✅ Your communication style
- ✅ Words associated with your moods
- ✅ Your preferences and interests

## 📊 Check Your Progress

Click "View Stats" to see:
- Total conversations
- Topics learned
- Your saved name
- Learning milestones

## ⚠️ Important Notes

1. **Privacy**: All data stays on your computer
2. **Camera**: Only used for mood detection at session start
3. **Storage**: AI knowledge files are small (usually < 1MB)
4. **Reset**: Delete data files anytime to reset the AI

## 🎉 You're Ready!

Now start the application and enjoy your personalized AI companion!

```bash
python CoconutAi.py
```

Happy chatting! 🥥🤖
