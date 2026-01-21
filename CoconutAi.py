import cv2
import tkinter as tk
from tkinter import messagebox, scrolledtext
from deepface import DeepFace
import pyttsx3
import time
from PIL import Image, ImageTk
import json
import os
from datetime import datetime
import random
import re
from collections import defaultdict
import pickle
import math

# =========================
# SELF-LEARNING AI SYSTEM
# =========================

class SelfLearningAI:
    """
    A self-learning AI system that adapts responses based on user interactions
    and mood patterns. It learns from conversations and improves over time.
    """
    
    def __init__(self):
        self.knowledge_base = self.load_knowledge()
        self.conversation_history = []
        self.user_preferences = self.load_preferences()
        self.mood_patterns = defaultdict(list)
        self.response_feedback = defaultdict(int)
        
    def load_knowledge(self):
        """Load existing knowledge from file or create new"""
        if os.path.exists('ai_knowledge.pkl'):
            with open('ai_knowledge.pkl', 'rb') as f:
                return pickle.load(f)
        return {
            'patterns': defaultdict(list),
            'responses': defaultdict(list),
            'mood_responses': self.get_default_mood_responses(),
            'learned_topics': {},
            'word_associations': defaultdict(list)
        }
    
    def get_default_mood_responses(self):
        """Default responses based on mood"""
        return {
            'happy': [
                "That's wonderful! I'm glad you're feeling great! 😊",
                "Your positive energy is contagious! Tell me more!",
                "I love seeing you so happy! What's making your day special?"
            ],
            'sad': [
                "I'm here for you. Would you like to talk about what's bothering you?",
                "I understand you're feeling down. Remember, this too shall pass.",
                "It's okay to feel sad sometimes. I'm listening if you want to share."
            ],
            'angry': [
                "I can sense you're upset. Let's work through this together.",
                "Take a deep breath. I'm here to help you feel better.",
                "I understand you're frustrated. Tell me what happened."
            ],
            'neutral': [
                "How can I assist you today?",
                "I'm here to chat. What's on your mind?",
                "Feel free to share anything with me."
            ],
            'surprise': [
                "Oh! Something unexpected happened? Tell me about it!",
                "Wow! I'd love to hear what surprised you!",
                "That sounds interesting! What's going on?"
            ],
            'fear': [
                "It's okay to feel anxious. I'm here with you.",
                "Let's talk about what's worrying you. You're safe here.",
                "I'm here to support you. What can I do to help?"
            ],
            'disgust': [
                "I understand that something's bothering you. Want to talk about it?",
                "That sounds unpleasant. How can I help you feel better?",
                "I'm listening. Tell me what's on your mind."
            ]
        }
    
    def load_preferences(self):
        """Load user preferences"""
        if os.path.exists('user_preferences.json'):
            with open('user_preferences.json', 'r') as f:
                return json.load(f)
        return {'name': None, 'interests': [], 'conversation_style': 'friendly'}
    
    def save_knowledge(self):
        """Save learned knowledge to file"""
        with open('ai_knowledge.pkl', 'wb') as f:
            pickle.dump(self.knowledge_base, f)
    
    def save_preferences(self):
        """Save user preferences"""
        with open('user_preferences.json', 'w') as f:
            json.dump(self.user_preferences, f, indent=2)
    
    def learn_from_input(self, user_input, mood):
        """Learn patterns and associations from user input"""
        # Store conversation in history
        self.conversation_history.append({
            'input': user_input,
            'mood': mood,
            'timestamp': datetime.now().isoformat()
        })
        
        # Extract keywords and learn associations
        words = re.findall(r'\b\w+\b', user_input.lower())
        for word in words:
            if len(word) > 3:  # Ignore short words
                self.knowledge_base['word_associations'][word].append(mood)
        
        # Learn mood patterns
        self.mood_patterns[mood].append(user_input)
        
        # Learn topics mentioned
        topics = self.extract_topics(user_input)
        for topic in topics:
            if topic not in self.knowledge_base['learned_topics']:
                self.knowledge_base['learned_topics'][topic] = []
            self.knowledge_base['learned_topics'][topic].append({
                'context': user_input,
                'mood': mood,
                'timestamp': datetime.now().isoformat()
            })
        
        # Save learned data periodically
        if len(self.conversation_history) % 5 == 0:
            self.save_knowledge()
            self.save_preferences()
    
    def extract_topics(self, text):
        """Extract potential topics from text"""
        # Common topics to look for
        topic_keywords = {
            'work': ['work', 'job', 'office', 'career', 'project'],
            'family': ['family', 'mom', 'dad', 'sister', 'brother', 'parent'],
            'friends': ['friend', 'buddy', 'pal', 'companion'],
            'health': ['health', 'sick', 'doctor', 'exercise', 'fitness'],
            'hobby': ['hobby', 'game', 'play', 'fun', 'enjoy'],
            'food': ['food', 'eat', 'hungry', 'meal', 'dinner', 'lunch'],
            'weather': ['weather', 'rain', 'sunny', 'cold', 'hot'],
            'love': ['love', 'relationship', 'girlfriend', 'boyfriend', 'partner']
        }
        
        topics = []
        text_lower = text.lower()
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        return topics
    
    def solve_math(self, user_input):
        """Solve mathematical expressions safely"""
        try:
            # Extract mathematical expression
            # Look for patterns like "what is 5+5", "calculate 10*2", "solve 100/4"
            math_patterns = [
                r'what\s+is\s+([\d+\-*/().\s]+)',
                r'calculate\s+([\d+\-*/().\s]+)',
                r'solve\s+([\d+\-*/().\s]+)',
                r'what\'?s\s+([\d+\-*/().\s]+)',
                r'^([\d+\-*/().\s]+)={0,1}\??$'
            ]
            
            expression = None
            for pattern in math_patterns:
                match = re.search(pattern, user_input.lower())
                if match:
                    expression = match.group(1).strip()
                    break
            
            if not expression:
                return None
            
            # Remove any trailing question marks or equals signs
            expression = expression.rstrip('?=').strip()
            
            # Safety check: only allow numbers, basic operators, parentheses, and decimal points
            if not re.match(r'^[\d+\-*/().\s]+$', expression):
                return None
            
            # Evaluate safely using eval with restricted namespace
            safe_dict = {
                '__builtins__': {},
                'abs': abs,
                'round': round,
                'min': min,
                'max': max,
                'pow': pow,
                'sqrt': math.sqrt,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
            }
            
            result = eval(expression, safe_dict)
            
            # Format the response
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 6)
            
            return f"The answer is {result}! 🧮 (Calculated: {expression} = {result})"
            
        except Exception as e:
            return None
    
    def generate_response(self, user_input, mood):
        """Generate intelligent response based on mood and learned patterns"""
        # Learn from this interaction
        self.learn_from_input(user_input, mood)
        
        # Check for specific patterns
        user_input_lower = user_input.lower()
        
        # Check for math questions first
        math_response = self.solve_math(user_input)
        if math_response:
            return math_response
        
        # Personal questions
        if any(word in user_input_lower for word in ['your name', 'who are you', 'what are you']):
            return "I'm CoconuTAi, your mood-aware AI companion! I learn from our conversations to better understand and help you."
        
        if 'my name is' in user_input_lower:
            name = user_input_lower.split('my name is')[-1].strip().split()[0]
            self.user_preferences['name'] = name.capitalize()
            self.save_preferences()
            return f"Nice to meet you, {name.capitalize()}! I'll remember that. 😊"
        
        # Check for learned topics
        topics = self.extract_topics(user_input)
        if topics and random.random() > 0.5:  # Sometimes use topic knowledge
            topic = topics[0]
            if topic in self.knowledge_base['learned_topics']:
                return f"I remember you've mentioned {topic} before. {self.get_mood_response(mood)}"
        
        # Use name if known
        greeting = ""
        if self.user_preferences['name'] and random.random() > 0.7:
            greeting = f"{self.user_preferences['name']}, "
        
        # Generate mood-based response with learning
        base_response = self.get_mood_response(mood)
        
        # Add contextual response based on input
        if '?' in user_input:
            return greeting + self.handle_question(user_input, mood)
        elif any(word in user_input_lower for word in ['thank', 'thanks']):
            return greeting + "You're very welcome! I'm always here to help. 💙"
        elif any(word in user_input_lower for word in ['hello', 'hi', 'hey']):
            return greeting + f"Hello! {base_response}"
        else:
            return greeting + self.generate_contextual_response(user_input, mood, base_response)
    
    def get_mood_response(self, mood):
        """Get appropriate response based on mood"""
        mood_responses = self.knowledge_base['mood_responses'].get(mood, self.knowledge_base['mood_responses']['neutral'])
        return random.choice(mood_responses)
    
    def handle_question(self, question, mood):
        """Handle questions intelligently"""
        question_lower = question.lower()
        
        if 'how are you' in question_lower:
            return "I'm doing great, thanks for asking! How about you?"
        elif 'help' in question_lower:
            return f"I'm here to help! {self.get_mood_response(mood)} What do you need assistance with?"
        elif 'can you' in question_lower:
            return "I'll do my best to help! I'm learning every day to serve you better. What do you need?"
        else:
            responses = [
                f"That's an interesting question! {self.get_mood_response(mood)}",
                f"Let me think about that... {self.get_mood_response(mood)}",
                f"Good question! {self.get_mood_response(mood)}"
            ]
            return random.choice(responses)
    
    def generate_contextual_response(self, user_input, mood, base_response):
        """Generate response with context awareness"""
        # Sentiment-based responses
        positive_words = ['love', 'great', 'awesome', 'wonderful', 'excellent', 'happy']
        negative_words = ['hate', 'bad', 'terrible', 'awful', 'sad', 'upset']
        
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in positive_words):
            return f"I can feel your positivity! {base_response} Tell me more about what makes you feel this way!"
        elif any(word in user_input_lower for word in negative_words):
            return f"I understand you're going through something difficult. {base_response}"
        else:
            responses = [
                f"{base_response} Tell me more about that!",
                f"I hear you. {base_response}",
                f"Interesting! {base_response}",
                f"{base_response} How does that make you feel?"
            ]
            return random.choice(responses)
    
    def get_conversation_stats(self):
        """Get statistics about conversations"""
        return {
            'total_conversations': len(self.conversation_history),
            'topics_learned': len(self.knowledge_base['learned_topics']),
            'mood_encounters': dict(self.mood_patterns),
            'user_name': self.user_preferences.get('name', 'Unknown')
        }

# Initialize the AI system
ai_system = SelfLearningAI()

# Function to display the logo in the tkinter window
def display_logo():
    logo = ''' 
    CoconuTAi
    Your AI Chatbot with Mood Detection
    '''
    return logo

# Initialize the text-to-speech engine
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to capture face and detect mood
def detect_mood():
    # Start video capture (Camera)
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("Error: Could not access the camera.")
        return None
    
    print("Camera opened successfully!")

    # Give the user a few seconds to prepare
    time.sleep(2)

    # Capture a frame from the camera
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to grab frame.")
        return None

    # Use DeepFace to analyze the image for mood detection
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        dominant_emotion = result[0]['dominant_emotion']
    except Exception as e:
        print("Error in face detection:", e)
        return None

    video_capture.release()  # Release the camera

    print(f"Detected mood: {dominant_emotion}")
    return dominant_emotion

# Function to start chatbot in the dialog box
def start_chatbot(mood, root):
    def send_message(event=None):
        user_input = user_input_entry.get()
        if not user_input.strip():
            return
            
        if user_input.lower() in ['exit', 'quit', 'bye']:
            stats = ai_system.get_conversation_stats()
            goodbye_msg = f"Goodbye! We've had {stats['total_conversations']} conversations. "
            if stats['user_name'] != 'Unknown':
                goodbye_msg += f"See you later, {stats['user_name']}! 👋"
            else:
                goodbye_msg += "Take care! 👋"
            
            messagebox.showinfo("Chatbot", goodbye_msg)
            ai_system.save_knowledge()
            ai_system.save_preferences()
            root.quit()
        else:
            # Display user message
            chatbox.config(state='normal')
            chatbox.insert(tk.END, f"You: {user_input}\n", 'user')
            user_input_entry.delete(0, tk.END)
            
            # Generate AI response using self-learning system
            response = ai_system.generate_response(user_input, mood)
            chatbox.insert(tk.END, f"CoconuTAi: {response}\n\n", 'bot')
            chatbox.config(state='disabled')
            chatbox.see(tk.END)
            
            # Speak the response
            speak(response)
    
    # Configure chatbox tags for better formatting
    chatbox.tag_config('user', foreground='#2E86AB', font=('Helvetica', 10, 'bold'))
    chatbox.tag_config('bot', foreground='#06A77D', font=('Helvetica', 10))
    
    chatbox.config(state='normal')
    chatbox.delete(1.0, tk.END)  # Clear the chatbox at the start
    
    # Personalized greeting
    greeting = "CoconuTAi: "
    if ai_system.user_preferences['name']:
        greeting += f"Welcome back, {ai_system.user_preferences['name']}! "
    else:
        greeting += "Hello! "
    
    greeting += f"I detected that you're feeling {mood}. How can I assist you today?\n\n"
    chatbox.insert(tk.END, greeting, 'bot')
    
    # Mood-specific initial message
    initial_response = ai_system.get_mood_response(mood)
    chatbox.insert(tk.END, f"CoconuTAi: {initial_response}\n\n", 'bot')
    chatbox.config(state='disabled')
    
    # Speak initial greeting
    if mood in ['happy', 'neutral']:
        speak("You seem to be in a good mood! Let me assist you.")
    elif mood in ['sad', 'angry', 'fear']:
        speak("I'm here for you. Let me help you feel better.")
    else:
        speak(f"I detected you're feeling {mood}. How can I help?")
    
    # Bind Enter key to send message
    user_input_entry.bind('<Return>', send_message)
    
    # Update send button command
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button) and widget.cget('text') == 'Send':
            widget.destroy()
    
    send_button = tk.Button(root, text="Send", command=send_message, bg='#06A77D', fg='white', 
                           font=('Helvetica', 10, 'bold'), padx=20, pady=5)
    send_button.pack(pady=10)

# Function to update GUI with the mood detection results
def show_mood_and_chat(root):
    mood = detect_mood()
    
    if mood:
        speak(f"Your detected mood is {mood}")
        mood_label.config(text=f"Detected Mood: {mood}")
        
        # Show chatbot window for user interaction
        start_chatbot(mood, root)

# Create the main application window
root = tk.Tk()
root.title("CoconuTAi - Mood Detection and Self-Learning Chatbot")
root.geometry("700x750")
root.configure(bg='#F0F4F8')

# Display logo as a label with enhanced styling
logo = display_logo()
logo_label = tk.Label(root, text=logo, font=("Helvetica", 18, "bold"), 
                     bg='#F0F4F8', fg='#2E86AB')
logo_label.pack(pady=15)

# Add a label for mood display with better styling
mood_label = tk.Label(root, text="Ready to detect your mood...", 
                     font=("Helvetica", 12), bg='#F0F4F8', fg='#555555')
mood_label.pack(pady=10)

# Add info label about AI learning
info_label = tk.Label(root, text="🧠 This AI learns from every conversation to serve you better!", 
                     font=("Helvetica", 9, "italic"), bg='#F0F4F8', fg='#06A77D')
info_label.pack(pady=5)

# Add a button to start the mood detection process with better styling
start_button = tk.Button(root, text="🎭 Start Mood Detection", command=lambda: show_mood_and_chat(root),
                        bg='#2E86AB', fg='white', font=('Helvetica', 12, 'bold'), 
                        padx=30, pady=10, relief=tk.RAISED, borderwidth=3)
start_button.pack(pady=20)

# Create a scrollable chatbox for chatbot interactions with better styling
chatbox_frame = tk.Frame(root, bg='#F0F4F8')
chatbox_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

chatbox = scrolledtext.ScrolledText(chatbox_frame, width=70, height=15, 
                                   wrap=tk.WORD, bg='#FFFFFF', 
                                   font=('Helvetica', 10), relief=tk.GROOVE, borderwidth=2)
chatbox.pack(fill=tk.BOTH, expand=True)
chatbox.config(state='disabled')

# Create a text entry box for user to type input with better styling
entry_frame = tk.Frame(root, bg='#F0F4F8')
entry_frame.pack(pady=10, padx=20, fill=tk.X)

user_input_entry = tk.Entry(entry_frame, width=50, font=('Helvetica', 11), 
                           relief=tk.GROOVE, borderwidth=2)
user_input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

# Stats button to view learning progress
def show_stats():
    stats = ai_system.get_conversation_stats()
    stats_msg = f"""
    📊 AI Learning Statistics 📊
    
    Total Conversations: {stats['total_conversations']}
    Topics Learned: {stats['topics_learned']}
    User: {stats['user_name']}
    
    The AI has been learning from your interactions!
    """
    messagebox.showinfo("Learning Progress", stats_msg)

stats_button = tk.Button(root, text="📊 View Stats", command=show_stats,
                        bg='#A23B72', fg='white', font=('Helvetica', 9, 'bold'), 
                        padx=15, pady=5)
stats_button.pack(pady=5)

# Run the tkinter main loop
root.mainloop()
