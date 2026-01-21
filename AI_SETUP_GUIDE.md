# 🤖 Setting Up Intelligent AI with Google Gemini (FREE)

Your CocoNUT AI is now powered by Google Gemini - a powerful, free AI that can:
- ✅ Help with coding in any language
- ✅ Answer complex questions
- ✅ Explain technical concepts
- ✅ Solve math problems
- ✅ Search the web for current information
- ✅ Understand context and mood

## 🆓 Get Your FREE API Key (2 Minutes)

### Step 1: Visit Google AI Studio
Go to: **https://makersuite.google.com/app/apikey**

### Step 2: Sign In
- Sign in with your Google account
- (Create one if you don't have it - it's free!)

### Step 3: Create API Key
1. Click **"Create API Key"** button
2. Select a project (or create new one)
3. Copy the API key (looks like: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXX`)

### Step 4: Set Environment Variable

#### On Windows (PowerShell):
```powershell
# Temporary (for current session):
$env:GEMINI_API_KEY="your_api_key_here"

# Permanent (recommended):
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'your_api_key_here', 'User')
```

#### On Windows (CMD):
```cmd
set GEMINI_API_KEY=your_api_key_here
```

#### On Linux/Mac:
```bash
export GEMINI_API_KEY="your_api_key_here"

# To make it permanent, add to ~/.bashrc or ~/.zshrc:
echo 'export GEMINI_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### Step 5: Restart Your Application
```bash
# Stop the current app (Ctrl+C)
# Then restart:
python app.py
```

You should see: ✅ **Google Gemini AI enabled**

---

## 🚀 What Your AI Can Do Now

### 1. Coding Help
```
You: "Write a Python function to reverse a string"
AI: *provides complete working code with explanation*

You: "How do I fix this error: TypeError: list indices must be integers"
AI: *explains the error and shows how to fix it*

You: "Create a REST API with Flask"
AI: *provides complete code with explanations*
```

### 2. Technical Questions
```
You: "Explain how async/await works in JavaScript"
AI: *detailed explanation with examples*

You: "What's the difference between SQL and NoSQL?"
AI: *comprehensive comparison*
```

### 3. Problem Solving
```
You: "How do I optimize my database queries?"
AI: *specific optimization techniques*

You: "Design a system for file uploads"
AI: *complete system design*
```

### 4. Current Information (with Web Search)
```
You: "What's the weather like today?"
AI: *searches web and provides answer*

You: "Latest news on AI"
AI: *finds and summarizes current information*
```

### 5. Math & Calculations
```
You: "Calculate 45 * 67 + 89"
AI: *solves and explains*

You: "What is the square root of 144?"
AI: *provides answer*
```

---

## ⚡ Free Tier Limits

Google Gemini FREE tier includes:
- ✅ **60 requests per minute**
- ✅ **Unlimited daily requests**
- ✅ **No credit card required**
- ✅ **Full model capabilities**

This is more than enough for personal use!

---

## 🔄 Without API Key (Fallback Mode)

If you don't set the API key, the chatbot will still work with basic responses:
- ⚠️ Limited to simple pattern matching
- ⚠️ No coding help
- ⚠️ No web search
- ⚠️ Basic mood-aware responses only

**We highly recommend getting the FREE API key for full functionality!**

---

## 🧪 Test Your Setup

After setting up, test these commands:

### Test 1: Basic Hello
```
You: "Hello"
AI: Should respond naturally based on your mood
```

### Test 2: Coding Question
```
You: "Write a Python function to find prime numbers"
AI: Should provide complete working code
```

### Test 3: Technical Question
```
You: "Explain what is REST API"
AI: Should give detailed explanation
```

### Test 4: Web Search
```
You: "What is the weather today?"
AI: Should mention web search capability
```

---

## 🐛 Troubleshooting

### "Gemini API key not found"
- Make sure you set the environment variable correctly
- Variable name must be exactly: `GEMINI_API_KEY`
- Restart your terminal/application after setting

### "API Error" or "Invalid API Key"
- Check if your API key is correct
- Make sure there are no extra spaces
- Try regenerating the key in Google AI Studio

### Still Getting Basic Responses
- Verify environment variable: 
  ```powershell
  echo $env:GEMINI_API_KEY  # PowerShell
  echo %GEMINI_API_KEY%     # CMD
  ```
- Restart the application completely

---

## 📊 Features Comparison

| Feature | Without API | With Gemini API |
|---------|------------|-----------------|
| Basic Chat | ✅ | ✅ |
| Mood Awareness | ✅ | ✅ |
| Coding Help | ❌ | ✅ |
| Code Debugging | ❌ | ✅ |
| Technical Explanations | ❌ | ✅ |
| Web Search | ❌ | ✅ |
| Context Memory | Limited | ✅ |
| Natural Conversation | ❌ | ✅ |
| Math Problems | Basic | ✅ |
| Multi-language Support | ❌ | ✅ |

---

## 🎯 Quick Start Checklist

- [ ] Get API key from: https://makersuite.google.com/app/apikey
- [ ] Set GEMINI_API_KEY environment variable
- [ ] Restart terminal/PowerShell
- [ ] Run: `python app.py`
- [ ] Look for: "✅ Google Gemini AI enabled"
- [ ] Test with: "Write a hello world program in Python"
- [ ] Enjoy your intelligent AI assistant! 🎉

---

## 💡 Pro Tips

1. **Be Specific**: The more detailed your question, the better the answer
   - ❌ "code for sorting"
   - ✅ "Write a Python function to sort a list of dictionaries by a specific key"

2. **Ask for Explanations**: Don't just ask for code
   - "Explain how this bubble sort algorithm works step by step"

3. **Use Context**: Reference previous messages
   - "Can you optimize the code you just wrote?"

4. **Debug Help**: Share error messages
   - "I'm getting this error: [paste error]. Here's my code: [paste code]"

5. **Multiple Languages**: Gemini supports many programming languages
   - Python, JavaScript, Java, C++, Go, Rust, and more!

---

## 🔒 Privacy & Security

- Your API key is stored locally only
- Conversations are processed by Google's servers
- Your code and data are not stored permanently by Google
- Database stores conversations locally on your machine
- You can delete conversation history anytime

---

## 📚 Resources

- **Gemini API Docs**: https://ai.google.dev/docs
- **Get API Key**: https://makersuite.google.com/app/apikey
- **Rate Limits**: https://ai.google.dev/pricing
- **Examples**: https://ai.google.dev/examples

---

## 🎉 You're All Set!

Your CocoNUT AI is now a **fully functional intelligent assistant** that can:
- Write and debug code
- Answer technical questions  
- Search the web
- Understand context
- Adapt to your mood

**Get your FREE API key and unlock the full power! 🚀**

Questions? Just ask your AI - it can help with that too! 😄
