# 🤖 Setting Up Intelligent AI with Ollama (Local, Free)

Your CocoNUT AI now runs locally through Ollama. No cloud API keys needed.

## 🚀 Quick Start (5 minutes)

1) **Install Ollama**: https://ollama.com/download (start the service after install).

2) **Pull a model** (PowerShell/CMD):
```
ollama pull llama3:8b
```
On 8 GB VRAM, `llama3:8b` with the default quant works. If you want faster/lighter, pull `phi3.5:mini`.

3) **Set optional env vars** (only if you want to override defaults):
```
# default host is http://localhost:11434
set OLLAMA_HOST=http://localhost:11434
set OLLAMA_MODEL=llama3:8b
```

4) **Run the app**:
```
python app.py
```
You should see: ✅ `Ollama model ready: llama3:8b @ http://localhost:11434`

---

## What the AI can do
- Coding help with working examples
- Technical Q&A and explanations
- Math and reasoning
- Mood-aware responses
- Light web-context pulls for current info

---

## Troubleshooting
- **Ollama not reachable**: Make sure the Ollama app/service is running. On Windows, check the system tray or run `ollama list`.
- **Model not found**: Run `ollama pull llama3:8b` (or your chosen model) and retry.
- **Slow or OOM on 8 GB**: Try `ollama pull phi3.5:mini` or a `q4` quant of your chosen model.
- **Change model**: Set `OLLAMA_MODEL` to any pulled model name, e.g. `OLLAMA_MODEL=phi3.5:mini`.

---

## Feature matrix

| Feature | Without Ollama running | With Ollama running |
|---------|------------------------|---------------------|
| Basic chat | ⚠️ Limited fallback | ✅ Full
| Mood awareness | ✅ | ✅
| Coding help | ⚠️ Minimal | ✅ Detailed
| Web/search context | ⚠️ None | ✅ Included when available
| Context memory | Limited | ✅ Extended

---

## Quick tests
- "Hello" → should greet with mood awareness
- "Write a Python function to reverse a string" → should return code
- "Explain async/await in JS" → detailed explanation
- "Latest news on AI" → mentions web search context if needed

---

## Tips
- Be specific: the more detail, the better the answer.
- Share errors verbatim for debugging.
- Use the `OLLAMA_MODEL` env var to switch models (e.g., `phi3.5:mini` for speed, `qwen2.5:7b` for multilingual strength).

---

Your CocoNUT AI is now fully local and private—no external API keys required. If something feels off, make sure Ollama is running and the model is pulled. Enjoy! 🎉
