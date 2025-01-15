import cv2
import tkinter as tk
from tkinter import messagebox
from deepface import DeepFace
import pyttsx3
import time
from PIL import Image, ImageTk

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
    def send_message():
        user_input = user_input_entry.get()
        if user_input.lower() == 'exit':
            messagebox.showinfo("Chatbot", "Goodbye!")
            root.quit()
        else:
            chatbot_response = f"I hear you! Let's talk about {user_input}"
            chatbox.insert(tk.END, f"You: {user_input}\nChatbot: {chatbot_response}\n")
            user_input_entry.delete(0, tk.END)

    chatbox.delete(1.0, tk.END)  # Clear the chatbox at the start
    chatbox.insert(tk.END, f"Chatbot: How can I assist you today?\n")

    if mood in ['happy', 'neutral']:
        speak("You seem happy! Let me assist you.")
        chatbox.insert(tk.END, "Chatbot: You seem happy! Let me assist you.\n")
    elif mood in ['sad', 'angry', 'irritated']:
        speak("You seem upset. Let me help you calm down.")
        chatbox.insert(tk.END, "Chatbot: You seem upset. Let me help you calm down.\n")

    send_button = tk.Button(root, text="Send", command=send_message)
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
root.title("CoconuTAi - Mood Detection and Chatbot")

# Display logo as a label
logo = display_logo()
logo_label = tk.Label(root, text=logo, font=("Helvetica", 16))
logo_label.pack(pady=10)

# Add a label for mood display
mood_label = tk.Label(root, text="Detecting mood...", font=("Helvetica", 14))
mood_label.pack(pady=10)

# Add a button to start the mood detection process
start_button = tk.Button(root, text="Start Mood Detection", command=lambda: show_mood_and_chat(root))
start_button.pack(pady=20)

# Create a scrollable chatbox for chatbot interactions
chatbox = tk.Text(root, width=50, height=10)
chatbox.pack(pady=10)

# Create a text entry box for user to type input
user_input_entry = tk.Entry(root, width=50)
user_input_entry.pack(pady=10)

# Run the tkinter main loop
root.mainloop()
