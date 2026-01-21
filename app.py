from flask import Flask, render_template, request, jsonify, Response, session
import cv2
from deepface import DeepFace
import pyttsx3
import json
import os
from datetime import datetime
import random
import re
from collections import defaultdict
import pickle
import math
import base64
import numpy as np
import uuid
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import configuration
from config import GEMINI_API_KEY

# Import database modules
from database import (
    DatabaseConnection, 
    create_user, 
    get_user_by_username,
    start_conversation,
    log_message,
    log_mood,
    get_conversation_history,
    get_mood_trends,
    update_ai_knowledge,
    get_knowledge_by_topic
)

app = Flask(__name__)
app.secret_key = 'coconut-ai-secret-key-change-this-in-production'  # Change this!

# =========================
# SELF-LEARNING AI SYSTEM
# =========================

class IntelligentAI:
    """
    An intelligent AI agent powered by Google Gemini (free) that can help with:
    - Coding and programming in any language
    - Web searches for current information
    - General conversation and questions
    - Mood-aware responses
    """
    
    def __init__(self):
        self.conversation_history = []
        self.current_mood = 'neutral'
        self.context_window = []  # Last 10 messages for context
        
        # Initialize knowledge base for learning
        self.knowledge_base = {
            'word_associations': defaultdict(list),
            'learned_topics': {},
            'user_patterns': defaultdict(int),
            'mood_responses': {
                'happy': ['I\'m so glad you\'re feeling happy!', 'Your happiness is contagious!', 'That\'s wonderful to hear!'],
                'sad': ['I\'m here for you.', 'It\'s okay to feel sad sometimes.', 'I\'m listening if you want to talk.'],
                'angry': ['I understand your frustration.', 'Take a deep breath. I\'m here to help.', 'Let\'s work through this together.'],
                'neutral': ['How can I help you today?', 'I\'m here to assist!', 'What would you like to know?'],
                'surprise': ['That\'s interesting!', 'Tell me more!', 'I\'m curious to hear more!'],
                'fear': ['Everything will be okay.', 'I\'m here with you.', 'You\'re safe to express yourself here.'],
                'disgust': ['I understand how you feel.', 'That\'s a valid reaction.', 'Let\'s talk about it.']
            }
        }
        
        # Initialize mood patterns
        self.mood_patterns = defaultdict(list)
        
        # Initialize user preferences
        self.user_preferences = {
            'response_style': 'friendly',
            'detail_level': 'moderate',
            'preferred_topics': []
        }
        
        # Initialize Google Gemini API (FREE)
        self.gemini_api_key = GEMINI_API_KEY or os.getenv('GEMINI_API_KEY', '')
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.ai_enabled = True
            print("✅ Google Gemini AI enabled")
        else:
            self.model = None
            self.ai_enabled = False
            print("⚠️  Gemini API key not found. Using fallback mode.")
            print("   Get free API key from: https://makersuite.google.com/app/apikey")
            print("   Set GEMINI_API_KEY environment variable")
        
        self.system_context = """You are CoconutAI, a highly intelligent and helpful AI assistant.

**Your Capabilities:**
- 💻 **Coding Expert**: Help with any programming language, debug code, explain concepts
- 🌐 **Web-Aware**: Access to web search for current information
- 🧠 **Problem Solver**: Answer questions, provide explanations, solve problems
- 😊 **Mood-Aware**: Adapt responses based on user's emotional state
- 📚 **Knowledgeable**: Help with math, science, writing, and more

**Your Personality:**
- Friendly, supportive, and encouraging
- Technical but clear when explaining
- Empathetic and understanding
- Direct and helpful

**Guidelines:**
- For coding questions: Provide complete, working code with explanations
- For current events: Mention if you need web search
- For mood: Adjust tone based on user's detected emotion
- Be concise but thorough
"""
        
    def search_web(self, query):
        """Search the web for current information"""
        try:
            # Use DuckDuckGo for free web search
            search_url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(search_url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = []
                for result in soup.find_all('a', class_='result__a', limit=3):
                    results.append({
                        'title': result.get_text(),
                        'url': result.get('href', '')
                    })
                return results
            return []
        except Exception as e:
            print(f"Web search error: {e}")
            return []
    
    def needs_web_search(self, query):
        """Determine if query needs web search"""
        web_keywords = [
            'weather', 'news', 'current', 'today', 'latest', 'recent',
            'what is happening', 'what happened', 'update on', 'price of',
            'stock', 'score', 'result'
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in web_keywords)
    
    def generate_response(self, user_input, mood=None):
        """Generate intelligent response using Gemini AI"""
        if mood is None:
            mood = self.current_mood
        
        # Add to conversation history
        self.conversation_history.append({
            'role': 'user',
            'content': user_input,
            'mood': mood,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep context window (last 10 messages)
        if len(self.context_window) > 10:
            self.context_window.pop(0)
        self.context_window.append(f"User ({mood}): {user_input}")
        
        try:
            # Check if AI is enabled
            if not self.ai_enabled:
                return self.fallback_response(user_input, mood)
            
            # Check if web search is needed
            web_context = ""
            if self.needs_web_search(user_input):
                search_results = self.search_web(user_input)
                if search_results:
                    web_context = "\n\nWeb Search Results:\n"
                    for i, result in enumerate(search_results, 1):
                        web_context += f"{i}. {result['title']}\n"
            
            # Build context-aware prompt
            mood_context = f"\n\nUser's current mood: {mood}. Adjust your tone accordingly."
            conversation_context = "\n\nRecent conversation:\n" + "\n".join(self.context_window[-5:])
            
            full_prompt = f"""{self.system_context}
{mood_context}
{conversation_context}
{web_context}

User: {user_input}

Respond helpfully and naturally. If it's a coding question, provide complete working code."""
            
            # Generate response using Gemini
            response = self.model.generate_content(full_prompt)
            ai_response = response.text
            
            # Add AI response to context
            self.context_window.append(f"AI: {ai_response}")
            self.conversation_history.append({
                'role': 'assistant',
                'content': ai_response,
                'timestamp': datetime.now().isoformat()
            })
            
            return ai_response
            
        except Exception as e:
            print(f"AI Error: {e}")
            return self.fallback_response(user_input, mood)
    
    def fallback_response(self, user_input, mood):
        """Fallback response when AI is not available"""
        user_lower = user_input.lower()
        
        # Coding help detection
        code_keywords = ['code', 'program', 'function', 'class', 'debug', 'error', 'python', 'javascript', 'java', 'html', 'css']
        if any(keyword in user_lower for keyword in code_keywords):
            return f"I can help with coding! However, I need the Gemini API to provide detailed code solutions.\n\n" \
                   f"To enable full coding assistance:\n" \
                   f"1. Get a free API key from: https://makersuite.google.com/app/apikey\n" \
                   f"2. Set environment variable: GEMINI_API_KEY=your_key\n" \
                   f"3. Restart the application\n\n" \
                   f"For now, please describe your coding problem and I'll do my best to help with general guidance."
        
        # Weather detection
        if 'weather' in user_lower:
            return "I can check the weather for you! However, I need the Gemini API enabled for real-time information.\n\n" \
                   "Get your free API key from: https://makersuite.google.com/app/apikey"
        
        # Greetings
        if any(word in user_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            mood_responses = {
                'happy': "Hello! I can see you're in a great mood! How can I help you today? 😊",
                'sad': "Hello. I'm here for you. What's on your mind? ",
                'angry': "Hello. I sense you might be frustrated. How can I assist you?",
                'neutral': "Hello! How can I help you today?",
                'surprise': "Hello! You seem surprised! What's going on?",
                'fear': "Hello. It's okay, I'm here to help. What do you need?",
                'disgust': "Hello. How can I assist you today?"
            }
            return mood_responses.get(mood, "Hello! How can I help you today?")
        
        # Questions
        if '?' in user_input:
            return f"That's an interesting question! To provide you with accurate and detailed answers, " \
                   f"I recommend enabling the Gemini API (free). " \
                   f"Get your key from: https://makersuite.google.com/app/apikey\n\n" \
                   f"For now, I can still try to help - please tell me more about what you'd like to know!"
        
        # Default response based on mood
        mood_responses = {
            'happy': "That's wonderful to hear! Tell me more!  ",
            'sad': "I'm here to listen. Would you like to talk about it?",
            'angry': "I understand. Let's work through this together.",
            'neutral': "I'm listening. How can I assist you?",
            'surprise': "Wow! That sounds interesting!",
            'fear': "It's okay. I'm here to support you.",
            'disgust': "I understand. How can I help you feel better?"
        }
        return mood_responses.get(mood, "I'm here to help! How can I assist you?")
    
    def get_conversation_stats(self):
        """Get statistics about conversations"""
        return {
            'total_conversations': len(self.conversation_history),
            'ai_enabled': self.ai_enabled,
            'messages_count': len(self.context_window)
        }
        
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
                "That's wonderful! I'm glad you're feeling great!",
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
        self.conversation_history.append({
            'input': user_input,
            'mood': mood,
            'timestamp': datetime.now().isoformat()
        })
        
        words = re.findall(r'\b\w+\b', user_input.lower())
        for word in words:
            if len(word) > 3:
                self.knowledge_base['word_associations'][word].append(mood)
        
        self.mood_patterns[mood].append(user_input)
        
        topics = self.extract_topics(user_input)
        for topic in topics:
            if topic not in self.knowledge_base['learned_topics']:
                self.knowledge_base['learned_topics'][topic] = []
            self.knowledge_base['learned_topics'][topic].append({
                'context': user_input,
                'mood': mood,
                'timestamp': datetime.now().isoformat()
            })
        
        if len(self.conversation_history) % 5 == 0:
            self.save_knowledge()
            self.save_preferences()
    
    def extract_topics(self, text):
        """Extract potential topics from text"""
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
            
            expression = expression.rstrip('?=').strip()
            
            if not re.match(r'^[\d+\-*/().\s]+$', expression):
                return None
            
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
            
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 6)
            
            return f"The answer is {result}! (Calculated: {expression} = {result})"
            
        except Exception as e:
            return None
    
    def generate_response(self, user_input, mood=None):
        """Generate intelligent response based on mood and learned patterns"""
        if mood is None:
            mood = self.current_mood
            
        self.learn_from_input(user_input, mood)
        
        user_input_lower = user_input.lower()
        
        # Check for math expressions first
        math_response = self.solve_math(user_input)
        if math_response:
            return math_response
        
        # Handle basic identity questions
        if any(word in user_input_lower for word in ['your name', 'who are you', 'what are you']):
            return "I'm CoconutAI, your mood-aware AI companion powered by Google Gemini! I can help with coding, answer questions, search the web, and adapt to your emotions."
        
        # Handle name introduction
        if 'my name is' in user_input_lower:
            name = user_input_lower.split('my name is')[-1].strip().split()[0]
            self.user_preferences['name'] = name.capitalize()
            self.save_preferences()
            return f"Nice to meet you, {name.capitalize()}! I'll remember that."
        
        # Use Gemini AI for intelligent responses
        if self.ai_enabled:
            try:
                # Build context with mood awareness
                mood_context = f"\n\nUser's current mood: {mood}. Adjust your response tone accordingly - be empathetic and supportive."
                
                # Add conversation history for context
                context = self.system_context + mood_context
                if len(self.context_window) > 0:
                    context += "\n\nRecent conversation:\n"
                    for msg in self.context_window[-3:]:
                        context += f"User: {msg['input']}\nYou: {msg.get('response', '')}\n"
                
                # Generate response with Gemini
                prompt = f"{context}\n\nUser: {user_input}\n\nProvide a helpful, friendly response:"
                response = self.model.generate_content(prompt)
                
                ai_response = response.text.strip()
                
                # Update context window
                self.context_window.append({
                    'input': user_input,
                    'response': ai_response,
                    'mood': mood
                })
                if len(self.context_window) > 10:
                    self.context_window.pop(0)
                
                return ai_response
                
            except Exception as e:
                logger.error(f"Gemini AI error: {e}")
                # Fall through to fallback responses
        
        # Fallback responses if Gemini is not available
        greeting = ""
        if self.user_preferences.get('name') and random.random() > 0.7:
            greeting = f"{self.user_preferences['name']}, "
        
        base_response = self.get_mood_response(mood)
        
        if '?' in user_input:
            return greeting + self.handle_question(user_input, mood)
        elif any(word in user_input_lower for word in ['thank', 'thanks']):
            return greeting + "You're very welcome! I'm always here to help."
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
            'user_name': self.user_preferences.get('name', 'Guest')
        }

# Initialize AI system
ai_system = IntelligentAI()

# =========================
# Database Helper Functions
# =========================

def get_or_create_user():
    """Get or create user from session"""
    try:
        if 'user_id' not in session or session['user_id'] is None:
            # Create a guest user
            username = f"guest_{str(uuid.uuid4())[:8]}"
            user_id = create_user(username, preferences={'conversation_style': 'friendly'})
            session['user_id'] = user_id
            return user_id
        return session['user_id']
    except Exception as e:
        print(f"Error getting/creating user: {e}")
        return None

def get_or_create_conversation(user_id):
    """Get or create conversation from session"""
    try:
        if user_id is None:
            return None
            
        if 'conversation_id' not in session or session['conversation_id'] is None:
            session_id = session.get('session_id', str(uuid.uuid4()))
            conversation_id = start_conversation(user_id, session_id)
            session['conversation_id'] = conversation_id
            return conversation_id
        return session['conversation_id']
    except Exception as e:
        print(f"Error getting/creating conversation: {e}")
        return None

@app.route('/')
def index():
    # Initialize session if needed
    if 'user_id' not in session:
        session['user_id'] = None
        session['session_id'] = str(uuid.uuid4())
    
    # Test database connection on first load (optional - won't crash if DB unavailable)
    try:
        db_status = DatabaseConnection.test_connection()
    except Exception as e:
        logger.warning(f"Database connection test failed: {e}")
        db_status = False
    
    return render_template('index.html')

@app.route('/detect_mood', methods=['POST'])
def detect_mood():
    try:
        data = request.json
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        dominant_emotion = result[0]['dominant_emotion']
        confidence = result[0]['emotion'][dominant_emotion] / 100.0
        ai_system.current_mood = dominant_emotion
        
        # Log mood to database if user is logged in
        user_id = get_or_create_user()
        if user_id:
            log_mood(user_id, dominant_emotion, confidence, "Face detection")
        
        return jsonify({
            'success': True,
            'mood': dominant_emotion,
            'confidence': confidence,
            'message': f"I detected that you're feeling {dominant_emotion}."
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'mood': 'neutral'
        })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data['message']
        mood = ai_system.current_mood
        
        # Get or create user and conversation
        user_id = get_or_create_user()
        conversation_id = get_or_create_conversation(user_id)
        
        # Log user message
        if user_id and conversation_id:
            log_message(conversation_id, user_id, 'user', user_message, mood, None)
        
        # Generate AI response
        response = ai_system.generate_response(user_message, mood)
        
        # Log AI response
        if user_id and conversation_id:
            log_message(conversation_id, user_id, 'ai', response, None, None)
        
        return jsonify({
            'success': True,
            'response': response,
            'mood': mood
        })
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e),
            'response': "I'm sorry, I encountered an error. Please try again."
        })

@app.route('/stats', methods=['GET'])
def get_stats():
    stats = ai_system.get_conversation_stats()
    
    # Add database stats if user exists
    user_id = session.get('user_id')
    if user_id:
        try:
            # Get mood trends
            mood_data = get_mood_trends(user_id, days=7)
            stats['mood_trends'] = mood_data if mood_data else []
            
            # Get conversation history count
            history = get_conversation_history(user_id, limit=100)
            stats['message_count'] = len(history) if history else 0
        except Exception as e:
            print(f"Error getting database stats: {e}")
    
    return jsonify(stats)

@app.route('/reset', methods=['POST'])
def reset_session():
    ai_system.current_mood = 'neutral'
    # Clear session data but keep user_id for history
    session['conversation_id'] = None
    return jsonify({'success': True})

@app.route('/history', methods=['GET'])
def get_history():
    """Get conversation history for current user"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'error': 'No user session'})
    
    try:
        limit = request.args.get('limit', 50, type=int)
        history = get_conversation_history(user_id, limit)
        return jsonify({
            'success': True,
            'history': history if history else []
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/mood_trends', methods=['GET'])
def get_mood_trends_route():
    """Get mood trends for current user"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'error': 'No user session'})
    
    try:
        days = request.args.get('days', 7, type=int)
        trends = get_mood_trends(user_id, days)
        return jsonify({
            'success': True,
            'trends': trends if trends else []
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/test_db', methods=['GET'])
def test_db():
    """Test database connection"""
    try:
        success = DatabaseConnection.test_connection()
        return jsonify({
            'success': success,
            'message': 'Database connection successful!' if success else 'Database connection failed!'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    # Use environment variable for port (for Cloud Run compatibility)
    port = int(os.environ.get('PORT', 5000))
    # Debug mode off in production
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
