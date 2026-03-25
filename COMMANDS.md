# CoconuT-Ai Commands

## 1. Install Dependencies (run once)
```powershell
pip install -r requirements.txt
```

## 2. Pull Ollama Model (run once)
```powershell
ollama pull qwen2.5:7b
```

## 3. Run the App
```powershell
python app.py
```
Then open: http://localhost:5000

## 4. Stop the App
Press `Ctrl + C` in the terminal.

## 5. Run with Specific Ollama Model
```powershell
$env:OLLAMA_MODEL="qwen2.5:7b"; python app.py
```

## 6. Check Ollama Status
```powershell
ollama list
```
