<div align="center">
  <img src="https://i.imgur.com/6fImgCg.png" alt="CoconuT-Ai Logo" width="150"/>
  <h1>CoconuT-Ai 🥥🤖</h1>
  <p><strong>Your Enterprise-Grade Emotion AI & Conversational Intelligence Platform</strong></p>
  
  <p>
    <a href="#-key-features">Features</a> •
    <a href="#-live-demonstration">Live Demo</a> •
    <a href="#-technology-stack">Tech Stack</a> •
    <a href="#-getting-started">Installation</a> •
    <a href="#-usage">Usage</a> •
    <a href="#-license">License</a>
  </p>

  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
  [![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![Framework](https://img.shields.io/badge/Framework-Flask-red.svg)](https://flask.palletsprojects.com/)

</div>

**CoconuT-Ai** is a sophisticated, self-learning AI platform that provides deep emotional analysis and personalized, context-aware conversational experiences. Designed for a premium user experience, it leverages real-time facial emotion recognition to deliver unparalleled human-computer interaction.

---

## ✨ Key Features

<details>
<summary><strong>🔬 Emotion AI Analysis</strong></summary>
<br>
<ul>
  <li><strong>Real-time Facial Recognition</strong>: Utilizes the DeepFace library to analyze facial expressions via webcam.</li>
  <li><strong>Multi-Dimensional Emotion Detection</strong>: Accurately identifies 7 core emotional states: happy, sad, angry, surprise, fear, disgust, and neutral.</li>
  <li><strong>Session Initiation</strong>: Begins each interaction with a precise emotional baseline analysis to tailor the conversation.</li>
</ul>
</details>

<details>
<summary><strong>🧠 Continuous Intelligence Engine</strong></summary>
<br>
<ul>
  <li><strong>Conversational Learning</strong>: The AI learns and adapts from every interaction, continuously improving its understanding and response accuracy.</li>
  <li><strong>In-Memory Knowledge Base</strong>: Maintains a dynamic, in-memory model of the conversation for immediate context recall.</li>
  <li><strong>Local-First LLM</strong>: Powered by Ollama and Llama3 for secure, on-device conversational generation.</li>
</ul>
</details>

<details>
<summary><strong>💬 Context-Aware Dialogue System</strong></summary>
<br>
<ul>
  <li><strong>Emotionally-Tuned Responses</strong>: Generates responses that are appropriate for the user's detected emotional state.</li>
  <li><strong>Sophisticated "Thinking" Animation</strong>: A professional UI animation indicates when the AI is processing and formulating a response.</li>
  <li><strong>Natural & Fluid Conversation</strong>: Manages conversational flow with context-aware replies and intelligent question handling.</li>
</ul>
</details>

<details>
<summary><strong>🎵 Audio Atmosphere</strong></summary>
<br>
<ul>
  <li><strong>Mood-Based Ambient Sound</strong>: Plays ambient background sounds (e.g., rain, forest) that correspond to the user's detected mood.</li>
  <li><strong>Integrated Music Player</strong>: Allows users to play curated songs during the session.</li>
  <li><strong>Independent Volume Controls</strong>: Separate controls for ambient sounds and music for a fully customizable audio experience.</li>
</ul>
</details>

<details>
<summary><strong>💼 Premium Enterprise UI</strong></summary>
<br>
<ul>
  <li><strong>Professional & Minimal Design</strong>: A clean, dark-themed interface built for a premium SaaS experience.</li>
  <li><strong>Intuitive Controls</strong>: Easy-to-use interface for starting analysis, sending messages, and controlling audio.</li>
  <li><strong>Analytics Dashboard</strong>: A modal providing insights into the AI's operational status and learned topics.</li>
</ul>
</details>

---

## 🎬 Live Demonstration

### Emotion Analysis & AI Chat
*This GIF demonstrates the initial emotion analysis, followed by a seamless transition to the conversational interface where the AI is actively responding.*

![Emotion Analysis and Chat GIF](https://i.imgur.com/M8dJ4aV.gif)

### Audio Atmosphere Controls
*This GIF showcases the user interacting with the ambient sound and music player controls.*

![Audio Controls GIF](https://i.imgur.com/O3bNcgt.gif)

---

## 🛠️ Technology Stack

| Category      | Technology                                                                                             |
|---------------|--------------------------------------------------------------------------------------------------------|
| **Backend**       | <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" /> <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" /> |
| **Frontend**      | <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" /> <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" /> <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" /> |
| **AI / ML**       | <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" /> `DeepFace` `Ollama` `Llama3` |
| **Database**      | `SQLite` (for persistent storage)                                                                      |
| **Deployment**    | `Dockerfile` `Gunicorn`                                                                                |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- A webcam for emotion analysis
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rohit27m/CoconuT-Ai.git
   cd CoconuT-Ai
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # For Windows
   python -m venv .venv
   .\.venv\Scripts\activate

   # For macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 📖 Usage

1. **Run the Flask application:**
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to `http://127.0.0.1:5000`.

3. **Click "Start Emotion Analysis"** and grant camera access when prompted.

4. Once your emotion is detected, the chat interface will appear. **Start your conversation!**

5. Use the **Audio Atmosphere** controls on the right to toggle ambient sounds and music.

---

## 🔒 Privacy

Your privacy is paramount.
- All data, including camera access and conversational logs, is processed and stored **locally on your machine**.
- No information is ever sent to external servers.
- The camera is used solely for the initial emotion detection and does not record.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/rohit27m/CoconuT-Ai/issues).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<div align="center">
  <p>Created with ❤️ by Rohit</p>
</div>
