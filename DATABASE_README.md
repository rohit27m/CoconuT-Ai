# CocoNUT AI Database Setup Guide

## Overview
This guide will help you set up the MySQL database for CocoNUT AI using XAMPP.

## Database Features
- **User Management**: Track users and their preferences
- **Conversation History**: Store all conversations and messages
- **Mood Tracking**: Log detected moods with confidence scores
- **AI Learning**: Store learned patterns and responses
- **Analytics**: View mood trends and conversation statistics

---

## Prerequisites

### 1. Install XAMPP
Download and install XAMPP from: https://www.apachefriends.org/

XAMPP includes:
- Apache Web Server
- MySQL Database
- PHP
- phpMyAdmin (Database management tool)

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

---

## Quick Setup (Recommended)

### Step 1: Start XAMPP
1. Open **XAMPP Control Panel**
2. Click **Start** next to **Apache**
3. Click **Start** next to **MySQL**
4. Both should show green status

### Step 2: Run Setup Script
```bash
python setup_database.py
```

Follow the prompts:
- **Host**: localhost (default)
- **Port**: 3306 (default)
- **User**: root (default)
- **Password**: (empty by default, just press Enter)

The script will:
- Create the `coconut_ai` database
- Create all required tables
- Insert default data
- Update your configuration file

### Step 3: Test Connection
```bash
python test_db.py
```

This will verify:
- Database connection works
- All tables are created
- Basic operations function correctly

### Step 4: Run the Application
```bash
python app.py
```

Visit: http://localhost:5000

---

## Manual Setup (Alternative)

If you prefer to set up manually:

### 1. Start XAMPP MySQL
Start MySQL service in XAMPP Control Panel

### 2. Access phpMyAdmin
Open your browser and go to: http://localhost/phpmyadmin

### 3. Import Database
1. Click on **"New"** in the left sidebar
2. Create database named: `coconut_ai`
3. Select the database
4. Click on **"Import"** tab
5. Choose file: `database.sql`
6. Click **"Go"** at the bottom

### 4. Verify Tables
You should see these tables created:
- users
- conversations
- messages
- mood_history
- ai_knowledge
- user_preferences
- response_feedback
- word_associations
- session_analytics
- learning_patterns

### 5. Update Configuration
Edit `config.py` with your MySQL credentials:
```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',  # Your password
    'database': 'coconut_ai',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': True,
    'raise_on_warnings': True
}
```

---

## Database Schema

### Main Tables

#### **users**
Stores user information and preferences
```sql
- user_id (Primary Key)
- username (Unique)
- email
- created_at
- last_active
- preferences (JSON)
```

#### **conversations**
Tracks conversation sessions
```sql
- conversation_id (Primary Key)
- user_id (Foreign Key)
- session_id
- started_at
- ended_at
- total_messages
```

#### **messages**
Stores all messages (user and AI)
```sql
- message_id (Primary Key)
- conversation_id (Foreign Key)
- user_id (Foreign Key)
- message_type (user/ai)
- message_text
- detected_mood
- mood_confidence
- timestamp
```

#### **mood_history**
Logs detected moods over time
```sql
- mood_id (Primary Key)
- user_id (Foreign Key)
- mood (happy, sad, angry, etc.)
- confidence
- context
- detected_at
```

#### **ai_knowledge**
Stores learned patterns and responses
```sql
- knowledge_id (Primary Key)
- topic
- pattern
- response
- usage_count
- success_rate
- created_at
- updated_at
```

### Analytics Views

#### **user_activity_summary**
Quick overview of user activity
```sql
SELECT * FROM user_activity_summary;
```

#### **mood_trends**
Analyze mood patterns over time
```sql
SELECT * FROM mood_trends WHERE user_id = 1;
```

#### **knowledge_performance**
View AI learning effectiveness
```sql
SELECT * FROM knowledge_performance;
```

---

## API Endpoints

Your Flask app now has database-enabled endpoints:

### Test Database
```
GET /test_db
```
Tests database connection

### Get Conversation History
```
GET /history?limit=50
```
Returns recent messages for current user

### Get Mood Trends
```
GET /mood_trends?days=7
```
Returns mood statistics for specified days

### Get Statistics
```
GET /stats
```
Returns conversation and mood statistics

---

## Troubleshooting

### Error: "Can't connect to MySQL server"
**Solution:**
1. Open XAMPP Control Panel
2. Make sure MySQL status is green (running)
3. Check if port 3306 is not blocked by firewall
4. Try: `netstat -ano | findstr :3306` to see if port is in use

### Error: "Access denied for user 'root'"
**Solution:**
1. Check password in `config.py`
2. Default XAMPP password is empty
3. If you changed the password, update `config.py`

### Error: "Database coconut_ai doesn't exist"
**Solution:**
Run the setup script:
```bash
python setup_database.py
```

### Error: "Import error: No module named mysql.connector"
**Solution:**
Install the MySQL connector:
```bash
pip install mysql-connector-python==8.2.0
```

### Tables Not Created
**Solution:**
1. Open phpMyAdmin: http://localhost/phpmyadmin
2. Manually import `database.sql`
3. Or run: `python setup_database.py`

### Connection Pool Error
**Solution:**
Restart the application:
```bash
# Stop the app (Ctrl+C)
python app.py
```

---

## Default Credentials

### XAMPP MySQL Default:
- **Host**: localhost
- **Port**: 3306
- **Username**: root
- **Password**: (empty)

### Default Test User:
- **Username**: guest
- **Email**: guest@coconutai.local

---

## Security Recommendations

For production use:

### 1. Change MySQL Password
```sql
-- In phpMyAdmin SQL tab:
ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_strong_password';
FLUSH PRIVILEGES;
```

### 2. Update config.py
```python
DB_CONFIG = {
    'password': 'your_strong_password',
    ...
}
```

### 3. Change Flask Secret Key
In `app.py`:
```python
app.secret_key = 'your-very-secret-random-key-here'
```

### 4. Create Dedicated Database User
```sql
CREATE USER 'coconut_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON coconut_ai.* TO 'coconut_user'@'localhost';
FLUSH PRIVILEGES;
```

Then update `config.py`:
```python
DB_CONFIG = {
    'user': 'coconut_user',
    'password': 'secure_password',
    ...
}
```

---

## Backup and Restore

### Backup Database
Using phpMyAdmin:
1. Go to: http://localhost/phpmyadmin
2. Select `coconut_ai` database
3. Click **Export** tab
4. Click **Go** (saves .sql file)

Using command line:
```bash
# In XAMPP mysql\bin directory
mysqldump -u root coconut_ai > backup.sql
```

### Restore Database
Using phpMyAdmin:
1. Select database
2. Click **Import** tab
3. Choose backup file
4. Click **Go**

Using command line:
```bash
mysql -u root coconut_ai < backup.sql
```

---

## Useful Commands

### View Logs
```python
# In Python console
from database import DatabaseConnection

# Test connection
DatabaseConnection.test_connection()

# View users
users = DatabaseConnection.execute_query("SELECT * FROM users", fetch=True)
print(users)

# View recent messages
messages = DatabaseConnection.execute_query(
    "SELECT * FROM messages ORDER BY timestamp DESC LIMIT 10",
    fetch=True
)
print(messages)
```

### Clear All Data (Keep Structure)
```sql
-- In phpMyAdmin SQL tab:
TRUNCATE TABLE messages;
TRUNCATE TABLE conversations;
TRUNCATE TABLE mood_history;
TRUNCATE TABLE users;
-- Repeat for other tables
```

### Reset Auto-Increment
```sql
ALTER TABLE users AUTO_INCREMENT = 1;
ALTER TABLE messages AUTO_INCREMENT = 1;
-- Repeat for other tables
```

---

## Database Maintenance

### Check Database Size
```sql
SELECT 
    table_schema AS 'Database',
    SUM(data_length + index_length) / 1024 / 1024 AS 'Size (MB)'
FROM information_schema.tables
WHERE table_schema = 'coconut_ai'
GROUP BY table_schema;
```

### Optimize Tables
```sql
OPTIMIZE TABLE users, conversations, messages, mood_history, ai_knowledge;
```

### View Table Status
```sql
SHOW TABLE STATUS FROM coconut_ai;
```

---

## Support

If you encounter issues:

1. Check XAMPP logs: `xampp/mysql/data/mysql_error.log`
2. Run test script: `python test_db.py`
3. Check application logs in console
4. Verify MySQL is running in XAMPP Control Panel

---

## Next Steps

After setting up the database:

1. ✅ Start the application: `python app.py`
2. ✅ Access web interface: http://localhost:5000
3. ✅ Test mood detection with webcam
4. ✅ Have conversations with the AI
5. ✅ View your mood trends: http://localhost:5000/mood_trends?days=7
6. ✅ Check conversation history: http://localhost:5000/history

---

## File Structure

```
CoconuT-Ai/
├── database.sql           # Database schema (all tables)
├── config.py             # Database configuration
├── database.py           # Database connection manager
├── setup_database.py     # Automated setup script
├── test_db.py           # Connection test script
├── app.py               # Flask web application (with DB integration)
├── requirements.txt      # Python dependencies
└── DATABASE_README.md   # This file
```

---

## Features Enabled

With database integration, you now have:

- ✅ Persistent user sessions
- ✅ Conversation history tracking
- ✅ Mood pattern analysis
- ✅ AI learning from interactions
- ✅ User preference storage
- ✅ Analytics and statistics
- ✅ Response feedback system
- ✅ Multi-user support

Enjoy your enhanced CocoNUT AI with full database capabilities! 🥥🤖
