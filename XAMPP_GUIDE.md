# 🎯 XAMPP Setup Guide for CocoNUT AI

## What is XAMPP?
XAMPP is a free software package that includes:
- **Apache** - Web server
- **MySQL** - Database server  
- **PHP** - Programming language
- **phpMyAdmin** - Database management tool

---

## 📥 Step 1: Download XAMPP

1. Go to: https://www.apachefriends.org/
2. Download XAMPP for Windows
3. Choose the latest version (PHP 8.x recommended)
4. File size: ~150 MB

---

## 💿 Step 2: Install XAMPP

1. Run the installer (`xampp-windows-x64-X.X.X-installer.exe`)
2. If Windows asks for permission, click **Yes**
3. If antivirus warning appears, allow the installation
4. Choose installation folder (default: `C:\xampp`)
5. Uncheck "Learn more about Bitnami" (optional)
6. Click **Next** through the installation
7. Click **Finish** when done

---

## 🚀 Step 3: Start XAMPP

### First Time Setup:
1. Open **XAMPP Control Panel** from Start Menu
   - Look for "XAMPP Control Panel" icon
   - Or run `C:\xampp\xampp-control.exe`

2. You'll see a window with several modules:
   ```
   Apache    [Start] [Admin] [Config]
   MySQL     [Start] [Admin] [Config]
   FileZilla [Start] [Admin] [Config]
   Mercury   [Start] [Admin] [Config]
   Tomcat    [Start] [Admin] [Config]
   ```

3. Click **Start** next to **Apache**
   - Status should turn **GREEN**
   - Port 80 and 443 will be used

4. Click **Start** next to **MySQL**
   - Status should turn **GREEN**
   - Port 3306 will be used

✅ **Success!** Both Apache and MySQL should show green status!

---

## 🔧 Step 4: Verify Installation

### Test Apache:
1. Open your web browser
2. Go to: `http://localhost`
3. You should see XAMPP welcome page

### Test MySQL:
1. Open your web browser
2. Go to: `http://localhost/phpmyadmin`
3. You should see phpMyAdmin interface

✅ If both work, XAMPP is installed correctly!

---

## 🐛 Troubleshooting

### ❌ Apache won't start (Port 80 in use)

**Problem**: Another program is using port 80 (often Skype or IIS)

**Solution 1** - Stop the conflicting program:
```bash
# Check what's using port 80
netstat -ano | findstr :80

# Find the process
tasklist | findstr <PID>

# Stop Skype/IIS from using port 80
```

**Solution 2** - Change Apache port:
1. In XAMPP Control Panel, click **Config** next to Apache
2. Select `httpd.conf`
3. Find line: `Listen 80`
4. Change to: `Listen 8080`
5. Find line: `ServerName localhost:80`
6. Change to: `ServerName localhost:8080`
7. Save and restart Apache
8. Access via: `http://localhost:8080`

### ❌ MySQL won't start (Port 3306 in use)

**Problem**: Another MySQL service is running

**Solution 1** - Stop other MySQL:
1. Open **Services** (Win + R, type `services.msc`)
2. Find "MySQL" or "MySQL80"
3. Right-click → Stop

**Solution 2** - Change MySQL port:
1. In XAMPP Control Panel, click **Config** next to MySQL
2. Select `my.ini`
3. Find line: `port=3306`
4. Change to: `port=3307`
5. Save and restart MySQL
6. Update `config.py` with new port

### ❌ "Cannot connect to MySQL server"

**Solution**:
1. Make sure MySQL is running (green in XAMPP)
2. Check Windows Firewall isn't blocking it
3. Try stopping and starting MySQL again

### ❌ phpMyAdmin Access Denied

**Solution**:
1. Default username: `root`
2. Default password: (empty)
3. If changed, update in `config.py`

---

## 🎨 Using phpMyAdmin

phpMyAdmin is a web interface for managing MySQL databases.

### Access phpMyAdmin:
```
http://localhost/phpmyadmin
```

### Create Database Manually:
1. Click **"New"** in left sidebar
2. Database name: `coconut_ai`
3. Collation: `utf8mb4_unicode_ci`
4. Click **"Create"**

### Import SQL File:
1. Select `coconut_ai` database
2. Click **"Import"** tab
3. Click **"Choose File"**
4. Select `database.sql`
5. Click **"Go"** at bottom
6. Wait for success message

### View Tables:
1. Select `coconut_ai` database
2. See all tables in left sidebar
3. Click any table to view data

### Run SQL Queries:
1. Click **"SQL"** tab
2. Type your query
3. Click **"Go"**

Example queries:
```sql
-- View all users
SELECT * FROM users;

-- View recent messages
SELECT * FROM messages ORDER BY timestamp DESC LIMIT 10;

-- View mood trends
SELECT mood, COUNT(*) as count FROM mood_history GROUP BY mood;
```

---

## 🔒 Security Settings (Optional)

### Set MySQL Root Password:
1. Open phpMyAdmin
2. Click **"User accounts"** tab
3. Click **"Edit privileges"** for `root@localhost`
4. Click **"Change password"**
5. Enter new password
6. Click **"Go"**

⚠️ **Important**: Update `config.py` after changing password!

```python
DB_CONFIG = {
    'password': 'your_new_password',
    ...
}
```

---

## 📊 XAMPP Control Panel Reference

### Buttons:
- **Start/Stop** - Start or stop a service
- **Admin** - Open service admin panel
  - Apache Admin → Opens localhost
  - MySQL Admin → Opens phpMyAdmin
- **Config** - Edit configuration files
- **Logs** - View error logs

### Ports:
| Service | Port | Purpose |
|---------|------|---------|
| Apache | 80 | Web server |
| Apache SSL | 443 | Secure web server |
| MySQL | 3306 | Database server |
| FileZilla | 21 | FTP server |
| Mercury | 25 | Mail server |
| Tomcat | 8080 | Java server |

---

## 🔄 Starting XAMPP on Boot (Optional)

### Auto-start Services:
1. Open XAMPP Control Panel
2. Click **Config** (top right)
3. Check **"Apache"** and **"MySQL"**
4. Click **"Save"**

Now Apache and MySQL will start automatically when Windows starts!

---

## 📁 Important Directories

### XAMPP Installation:
```
C:\xampp\
├── apache\        - Apache web server files
├── mysql\         - MySQL database files
│   └── data\      - Database storage
├── php\           - PHP files
├── phpMyAdmin\    - phpMyAdmin files
└── htdocs\        - Web root directory
```

### MySQL Data:
```
C:\xampp\mysql\data\coconut_ai\
```
All your database files are stored here

### Logs:
```
C:\xampp\mysql\data\mysql_error.log
C:\xampp\apache\logs\error.log
```

---

## ✅ Pre-Flight Checklist

Before running CocoNUT AI setup:

- [ ] XAMPP installed
- [ ] XAMPP Control Panel open
- [ ] Apache started (green status)
- [ ] MySQL started (green status)
- [ ] phpMyAdmin accessible at `http://localhost/phpmyadmin`
- [ ] Python installed
- [ ] Virtual environment activated (if using one)
- [ ] Requirements installed (`pip install -r requirements.txt`)

---

## 🎯 Next Steps

Once XAMPP is running:

1. Run database setup:
   ```bash
   python setup_database.py
   ```

2. Test connection:
   ```bash
   python test_db.py
   ```

3. Start application:
   ```bash
   python app.py
   ```

4. Open browser:
   ```
   http://localhost:5000
   ```

---

## 📞 Quick Commands

```bash
# Check if ports are in use
netstat -ano | findstr :80
netstat -ano | findstr :3306

# Stop XAMPP services (command line)
C:\xampp\apache_stop.bat
C:\xampp\mysql_stop.bat

# Start XAMPP services (command line)
C:\xampp\apache_start.bat
C:\xampp\mysql_start.bat

# Open XAMPP Control Panel
C:\xampp\xampp-control.exe

# Access phpMyAdmin
http://localhost/phpmyadmin

# Access XAMPP Dashboard
http://localhost
```

---

## 🆘 Need Help?

### XAMPP Documentation:
- https://www.apachefriends.org/faq_windows.html

### Common Issues:
- Port conflicts → Change ports in Config
- Permission issues → Run as Administrator
- Service won't start → Check Windows Services
- Database errors → Check MySQL error log

### CocoNUT AI Setup:
- See [DATABASE_QUICKSTART.md](DATABASE_QUICKSTART.md)
- See [DATABASE_README.md](DATABASE_README.md)
- See [DATABASE_SETUP_SUMMARY.md](DATABASE_SETUP_SUMMARY.md)

---

## 🎉 You're Ready!

With XAMPP running, you can now:
- ✅ Create MySQL databases
- ✅ Run web applications
- ✅ Manage databases with phpMyAdmin
- ✅ Run CocoNUT AI with database support

**Let's set up the database!** → Run `python setup_database.py`
