# 🏗️ CoconuT-Ai Architecture

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    COCONUT-AI SYSTEM                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                     │
├─────────────────────────────────────────────────────────────┤
│  • Tkinter GUI (700x750 window)                            │
│  • ScrolledText chatbox with color coding                   │
│  • Mood detection button                                    │
│  • Stats viewer                                             │
│  • Text entry with Enter key support                        │
│  • Text-to-Speech output (pyttsx3)                         │
└─────────────────────────────────────────────────────────────┘
                            ↓ ↑
┌─────────────────────────────────────────────────────────────┐
│                  MOOD DETECTION MODULE                       │
├─────────────────────────────────────────────────────────────┤
│  • OpenCV (Camera capture)                                  │
│  • DeepFace (Emotion analysis)                             │
│  • 7 Emotions: happy, sad, angry, neutral, surprise,       │
│                fear, disgust                                │
└─────────────────────────────────────────────────────────────┘
                            ↓ ↑
┌─────────────────────────────────────────────────────────────┐
│              SELF-LEARNING AI CORE (SelfLearningAI)        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────┐      │
│  │         INPUT PROCESSING                          │      │
│  ├──────────────────────────────────────────────────┤      │
│  │  • Text parsing (re module)                      │      │
│  │  • Keyword extraction                            │      │
│  │  • Sentiment analysis                            │      │
│  │  • Question detection                            │      │
│  └──────────────────────────────────────────────────┘      │
│                         ↓                                   │
│  ┌──────────────────────────────────────────────────┐      │
│  │         LEARNING ENGINE                           │      │
│  ├──────────────────────────────────────────────────┤      │
│  │  • Pattern recognition                           │      │
│  │  • Topic extraction (8+ categories)              │      │
│  │  • Word association learning                     │      │
│  │  • Mood correlation                              │      │
│  │  • Context building                              │      │
│  └──────────────────────────────────────────────────┘      │
│                         ↓                                   │
│  ┌──────────────────────────────────────────────────┐      │
│  │         RESPONSE GENERATION                       │      │
│  ├──────────────────────────────────────────────────┤      │
│  │  • Mood-based selection                          │      │
│  │  • Context-aware responses                       │      │
│  │  • Personalization (name, topics)                │      │
│  │  • Response variation (random)                   │      │
│  │  • Follow-up question generation                 │      │
│  └──────────────────────────────────────────────────┘      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                            ↓ ↑
┌─────────────────────────────────────────────────────────────┐
│                  MEMORY & PERSISTENCE LAYER                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────┐    ┌──────────────────────┐      │
│  │  Knowledge Base      │    │  User Preferences    │      │
│  │  (ai_knowledge.pkl)  │    │  (user_prefs.json)   │      │
│  ├─────────────────────┤    ├──────────────────────┤      │
│  │ • Patterns          │    │ • Name               │      │
│  │ • Responses         │    │ • Interests          │      │
│  │ • Topics            │    │ • Style              │      │
│  │ • Word associations │    │ • History            │      │
│  │ • Mood responses    │    │                      │      │
│  └─────────────────────┘    └──────────────────────┘      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
┌──────────┐
│  USER    │
└────┬─────┘
     │
     ↓
┌─────────────────┐
│ 1. Camera       │ → Capture face image
│    Activation   │
└────┬────────────┘
     │
     ↓
┌─────────────────┐
│ 2. Mood         │ → DeepFace analyzes emotion
│    Detection    │    (happy/sad/angry/etc.)
└────┬────────────┘
     │
     ↓
┌─────────────────────────────────────────┐
│ 3. Initial Greeting                     │
│    • Check if user name is known        │
│    • Select mood-appropriate greeting   │
│    • Display in chatbox                 │
│    • Speak greeting (TTS)               │
└────┬────────────────────────────────────┘
     │
     ↓
┌─────────────────────────────────────────┐
│ 4. User Input                           │
│    • User types message                 │
│    • Press Enter or click Send          │
└────┬────────────────────────────────────┘
     │
     ↓
┌─────────────────────────────────────────┐
│ 5. AI Processing                        │
│    ┌─────────────────────────────────┐  │
│    │ a. Parse Input                  │  │
│    │    • Extract words              │  │
│    │    • Identify keywords          │  │
│    └─────────┬───────────────────────┘  │
│              ↓                           │
│    ┌─────────────────────────────────┐  │
│    │ b. Learn from Input             │  │
│    │    • Store in history           │  │
│    │    • Extract topics             │  │
│    │    • Build associations         │  │
│    │    • Update patterns            │  │
│    └─────────┬───────────────────────┘  │
│              ↓                           │
│    ┌─────────────────────────────────┐  │
│    │ c. Context Analysis             │  │
│    │    • Check for name intro       │  │
│    │    • Detect questions           │  │
│    │    • Analyze sentiment          │  │
│    │    • Reference past topics      │  │
│    └─────────┬───────────────────────┘  │
│              ↓                           │
│    ┌─────────────────────────────────┐  │
│    │ d. Generate Response            │  │
│    │    • Select mood response       │  │
│    │    • Add personalization        │  │
│    │    • Include context            │  │
│    │    • Vary response style        │  │
│    └─────────┬───────────────────────┘  │
└──────────────┼─────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 6. Output                               │
│    • Display in chatbox (color coded)   │
│    • Speak response (TTS)               │
│    • Update conversation history        │
└────┬────────────────────────────────────┘
     │
     ↓
┌─────────────────────────────────────────┐
│ 7. Persistence                          │
│    • Auto-save every 5 conversations    │
│    • Save knowledge base                │
│    • Save user preferences              │
└────┬────────────────────────────────────┘
     │
     └─────→ (Loop back to step 4)
```

---

## Module Breakdown

### 1. **UI Module** (`tkinter`)
```python
Components:
- root: Main window (700x750)
- logo_label: Display title
- mood_label: Show detected mood
- chatbox: ScrolledText for chat history
- user_input_entry: Text input field
- send_button: Submit message
- stats_button: View learning progress
- start_button: Initiate mood detection
```

### 2. **Mood Detection Module**
```python
Functions:
- detect_mood()
  ├─ video_capture = cv2.VideoCapture(0)
  ├─ DeepFace.analyze(frame, actions=['emotion'])
  └─ Return: dominant_emotion

Emotions Detected:
- happy, sad, angry, neutral
- surprise, fear, disgust
```

### 3. **Self-Learning AI Module**
```python
Class: SelfLearningAI
├─ __init__(): Initialize AI system
├─ load_knowledge(): Load saved data
├─ save_knowledge(): Persist learning
├─ learn_from_input(): Process new input
├─ extract_topics(): Identify subjects
├─ generate_response(): Create reply
├─ handle_question(): Process questions
└─ get_conversation_stats(): Return metrics

Data Structures:
- knowledge_base: Dict[str, Any]
  ├─ patterns: defaultdict(list)
  ├─ responses: defaultdict(list)
  ├─ mood_responses: Dict[str, List[str]]
  ├─ learned_topics: Dict[str, List]
  └─ word_associations: defaultdict(list)

- conversation_history: List[Dict]
- user_preferences: Dict
- mood_patterns: defaultdict(list)
```

### 4. **NLP Module** (Integrated)
```python
Capabilities:
- Name extraction: "my name is X"
- Question detection: "?" in input
- Topic keywords: work, family, health, etc.
- Sentiment words: positive/negative lists
- Pattern matching: Regular expressions
```

### 5. **Memory Module**
```python
Files:
- ai_knowledge.pkl (pickle)
  └─ Stores: patterns, topics, associations

- user_preferences.json (JSON)
  └─ Stores: name, interests, style

Operations:
- Load on startup
- Auto-save every 5 conversations
- Manual save on exit
```

---

## Learning Algorithm Flow

```
┌────────────────────────────────────────┐
│  NEW USER INPUT                        │
└───────────┬────────────────────────────┘
            ↓
    ┌───────────────┐
    │ Word Parsing  │
    └───────┬───────┘
            ↓
    ┌─────────────────────────────────┐
    │ For each significant word:      │
    │  • Extract word (len > 3)       │
    │  • Associate with current mood  │
    │  • Store in word_associations   │
    └───────┬─────────────────────────┘
            ↓
    ┌─────────────────────────────────┐
    │ Topic Extraction:               │
    │  • Match against topic_keywords │
    │  • Identify: work, family, etc. │
    │  • Store context + timestamp    │
    └───────┬─────────────────────────┘
            ↓
    ┌─────────────────────────────────┐
    │ Pattern Recognition:            │
    │  • Store in mood_patterns       │
    │  • Build conversation history   │
    │  • Update knowledge base        │
    └───────┬─────────────────────────┘
            ↓
    ┌─────────────────────────────────┐
    │ Save if counter == 5            │
    └─────────────────────────────────┘
```

---

## Response Generation Algorithm

```
┌────────────────────────────────────────┐
│  generate_response(user_input, mood)   │
└───────────┬────────────────────────────┘
            ↓
    ┌───────────────────┐
    │ 1. Learn from     │ → Store input
    │    input first    │
    └───────┬───────────┘
            ↓
    ┌───────────────────────────────────┐
    │ 2. Check Special Patterns:        │
    │    • Name introduction?           │
    │    • Question about AI?           │
    │    • Gratitude expression?        │
    └───────┬───────────────────────────┘
            ↓ (if no match)
    ┌───────────────────────────────────┐
    │ 3. Check Learned Topics:          │
    │    • Extract topics from input    │
    │    • Find in learned_topics       │
    │    • Reference if found (50%)     │
    └───────┬───────────────────────────┘
            ↓
    ┌───────────────────────────────────┐
    │ 4. Add Personalization:           │
    │    • Use name if known (70%)      │
    │    • Add to greeting              │
    └───────┬───────────────────────────┘
            ↓
    ┌───────────────────────────────────┐
    │ 5. Response Type Selection:       │
    │    • Question? → handle_question  │
    │    • Thanks? → appreciation reply │
    │    • Greeting? → greeting reply   │
    │    • Other → contextual_response  │
    └───────┬───────────────────────────┘
            ↓
    ┌───────────────────────────────────┐
    │ 6. Apply Mood Filter:             │
    │    • Get base mood response       │
    │    • Analyze sentiment            │
    │    • Adjust tone                  │
    └───────┬───────────────────────────┘
            ↓
    ┌───────────────────────────────────┐
    │ 7. Return Final Response          │
    └───────────────────────────────────┘
```

---

## Statistics & Analytics

```
┌─────────────────────────────────────┐
│  get_conversation_stats()           │
├─────────────────────────────────────┤
│  Returns:                           │
│  {                                  │
│    'total_conversations': int,      │
│    'topics_learned': int,           │
│    'mood_encounters': dict,         │
│    'user_name': str                 │
│  }                                  │
└─────────────────────────────────────┘
```

---

## File Structure

```
CoconuT-Ai/
│
├── CoconutAi.py                 (458 lines - Main application)
│   ├── SelfLearningAI class    (250+ lines)
│   ├── UI functions             (100+ lines)
│   └── Helper functions         (100+ lines)
│
├── requirements.txt             (Dependencies)
├── README.md                    (Full documentation)
├── SETUP_GUIDE.md              (Installation guide)
├── EXAMPLE_CONVERSATIONS.md    (Usage examples)
├── ENHANCEMENT_SUMMARY.md      (Features overview)
├── ARCHITECTURE.md             (This file)
└── QUICK_START.txt             (Quick reference)

Generated at runtime:
├── ai_knowledge.pkl            (AI's learned data)
└── user_preferences.json       (User profile)
```

---

## Technology Stack

```
┌─────────────────────────────────────┐
│  FRONTEND                           │
├─────────────────────────────────────┤
│  • Tkinter (GUI)                   │
│  • ScrolledText (Chat display)      │
│  • pyttsx3 (Text-to-Speech)        │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  AI & COMPUTER VISION               │
├─────────────────────────────────────┤
│  • DeepFace (Emotion detection)     │
│  • TensorFlow (Backend for DL)      │
│  • OpenCV (Camera handling)         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  DATA & LEARNING                    │
├─────────────────────────────────────┤
│  • Pickle (Binary serialization)    │
│  • JSON (User preferences)          │
│  • Collections (Data structures)    │
│  • RE (Pattern matching)            │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  UTILITIES                          │
├─────────────────────────────────────┤
│  • datetime (Timestamps)            │
│  • random (Response variation)      │
│  • os (File operations)             │
└─────────────────────────────────────┘
```

---

## Performance Characteristics

### Memory Usage:
- Base application: ~50-100 MB
- DeepFace model: ~200-300 MB
- Knowledge base: <1 MB
- **Total**: ~300-400 MB

### Speed:
- Mood detection: 2-5 seconds
- Response generation: <100ms
- UI rendering: Real-time
- Auto-save: <50ms

### Scalability:
- Supports unlimited conversations
- Knowledge base grows linearly
- Efficient data structures (defaultdict)
- Periodic persistence (every 5 chats)

---

## Security & Privacy

```
┌─────────────────────────────────────┐
│  PRIVACY FEATURES                   │
├─────────────────────────────────────┤
│  ✓ Local storage only               │
│  ✓ No cloud uploads                 │
│  ✓ No external API calls            │
│  ✓ Camera used only when requested  │
│  ✓ User controls all data           │
│  ✓ Easy data deletion               │
└─────────────────────────────────────┘
```

---

**This architecture enables true self-learning AI with persistent memory!** 🧠✨
