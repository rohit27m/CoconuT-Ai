# 🥥 CocoNUT AI - Quick Database Setup

## 🚀 Quick Start (5 Minutes)

### Step 1: Start XAMPP
1. Open **XAMPP Control Panel**
2. Click **Start** for **Apache** ✓
3. Click **Start** for **MySQL** ✓

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup Database
```bash
python setup_database.py
```

When prompted:
- Host: `localhost` (just press Enter)
- Port: `3306` (just press Enter)
- User: `root` (just press Enter)
- Password: (just press Enter - empty by default)

### Step 4: Test Connection
```bash
python test_db.py
```

### Step 5: Run Application
```bash
python app.py
```

### Step 6: Open Browser
```
http://localhost:5000
```

## ✨ That's it! Your database is ready!

---

## 📊 What You Get

Your CocoNUT AI now has:
- ✅ **Persistent Conversations** - Never lose your chat history
- ✅ **Mood Tracking** - Analyze your emotions over time
- ✅ **AI Learning** - AI gets smarter with each conversation
- ✅ **User Profiles** - Multiple users supported
- ✅ **Analytics** - View trends and statistics

---

## 🔍 Quick Test

After running `python app.py`, test these URLs:

- **Main App**: http://localhost:5000
- **Test DB**: http://localhost:5000/test_db
- **Statistics**: http://localhost:5000/stats
- **History**: http://localhost:5000/history
- **Mood Trends**: http://localhost:5000/mood_trends?days=7

---

## 🐛 Troubleshooting

### MySQL won't start in XAMPP?
- Port 3306 might be in use
- Check Windows Task Manager for other MySQL processes
- Try changing port in XAMPP config

### Can't connect to database?
```bash
# Make sure MySQL is running
python test_db.py
```

### Import errors?
```bash
pip install mysql-connector-python==8.2.0
```

---

## 📖 Need More Help?

See [DATABASE_README.md](DATABASE_README.md) for:
- Detailed setup instructions
- Manual setup steps
- Database schema
- API documentation
- Security recommendations
- Backup/restore procedures

---

## 🎯 Files Created

Your project now has:
```
CoconuT-Ai/
├── database.sql           ← Database schema
├── config.py             ← DB configuration
├── database.py           ← Connection manager
├── setup_database.py     ← Setup script
├── test_db.py           ← Test script
├── app.py               ← Updated with DB integration
├── requirements.txt      ← Updated with mysql-connector
└── DATABASE_README.md    ← Full documentation
```

---

## 🎉 Ready to Use!

Your AI chatbot now saves:
- Every conversation
- Every detected mood
- Every learned pattern
- User preferences
- And more!

Start chatting and watch your AI learn! 🤖✨
