# =========================
# Database Configuration
# =========================
# Configure these settings for your XAMPP MySQL database

DB_CONFIG = {
    'host': 'localhost',        # XAMPP default host
    'port': 3306,               # XAMPP MySQL default port
    'user': 'root',             # XAMPP default username
    'password': '',             # XAMPP default password (empty by default)
    'database': 'coconut_ai',   # Database name from SQL schema
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': True,
    'raise_on_warnings': True
}

# Connection pool settings
POOL_CONFIG = {
    'pool_name': 'coconut_pool',
    'pool_size': 5,
    'pool_reset_session': True
}

# Database connection retry settings
RETRY_CONFIG = {
    'max_retries': 3,
    'retry_delay': 2  # seconds
}

# =========================
# API Configuration
# =========================
# Google Gemini API Key for AI capabilities
GEMINI_API_KEY = 'AIzaSyDuG2YCf-a5TVmITYm4giCxN7sZNnhnGQc'
