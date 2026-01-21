# =========================
# CocoNUT AI Database Setup
# =========================

"""
This script helps set up the database for CocoNUT AI

Prerequisites:
1. XAMPP must be installed and running
2. MySQL service must be started in XAMPP
3. Python MySQL connector must be installed (pip install mysql-connector-python)

Steps:
1. Start XAMPP Control Panel
2. Start Apache and MySQL services
3. Run this script to create the database
"""

import mysql.connector
from mysql.connector import Error
import os
import sys

def read_sql_file(filepath):
    """Read SQL file and return queries"""
    with open(filepath, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    return sql_content

def create_database():
    """Create the database and tables"""
    print("=" * 50)
    print("CocoNUT AI Database Setup")
    print("=" * 50)
    
    # Connection settings for XAMPP default
    host = input("Enter MySQL host (default: localhost): ").strip() or "localhost"
    port = input("Enter MySQL port (default: 3306): ").strip() or "3306"
    user = input("Enter MySQL user (default: root): ").strip() or "root"
    password = input("Enter MySQL password (press Enter if empty): ").strip()
    
    print("\n" + "=" * 50)
    print("Connecting to MySQL...")
    print("=" * 50)
    
    connection = None
    try:
        # Connect to MySQL server (without selecting database)
        connection = mysql.connector.connect(
            host=host,
            port=int(port),
            user=user,
            password=password
        )
        
        if connection.is_connected():
            print("✓ Successfully connected to MySQL server")
            cursor = connection.cursor()
            
            # Read and execute SQL file
            sql_file = 'database.sql'
            
            if not os.path.exists(sql_file):
                print(f"\n✗ Error: {sql_file} not found!")
                print(f"Please make sure {sql_file} is in the same directory as this script.")
                return False
            
            print(f"\n✓ Found {sql_file}")
            print("\n" + "=" * 50)
            print("Creating database and tables...")
            print("=" * 50)
            
            # Read SQL content
            sql_content = read_sql_file(sql_file)
            
            # Split by delimiter and execute
            statements = []
            current_statement = []
            in_delimiter_block = False
            
            for line in sql_content.split('\n'):
                line = line.strip()
                
                # Skip comments and empty lines
                if line.startswith('--') or not line:
                    continue
                
                # Handle DELIMITER changes
                if line.startswith('DELIMITER'):
                    in_delimiter_block = not in_delimiter_block
                    continue
                
                current_statement.append(line)
                
                # Check for statement end
                if in_delimiter_block:
                    if line.endswith('//'):
                        statements.append(' '.join(current_statement))
                        current_statement = []
                else:
                    if line.endswith(';'):
                        statements.append(' '.join(current_statement))
                        current_statement = []
            
            # Execute statements
            executed = 0
            for statement in statements:
                statement = statement.strip()
                if statement:
                    try:
                        # Handle multiple statements in one
                        for sub_statement in statement.split(';'):
                            sub_statement = sub_statement.strip()
                            if sub_statement:
                                cursor.execute(sub_statement)
                                executed += 1
                    except Error as e:
                        # Some statements may fail if already exist, that's ok
                        if "already exists" not in str(e).lower():
                            print(f"Warning: {e}")
            
            connection.commit()
            
            print(f"\n✓ Successfully executed {executed} SQL statements")
            print("\n" + "=" * 50)
            print("Verifying database...")
            print("=" * 50)
            
            # Verify tables were created
            cursor.execute("USE coconut_ai")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print(f"\n✓ Database 'coconut_ai' created successfully!")
                print(f"\n✓ Created {len(tables)} tables:")
                for table in tables:
                    print(f"  - {table[0]}")
                
                print("\n" + "=" * 50)
                print("Database setup complete!")
                print("=" * 50)
                print("\nYou can now run your application with:")
                print("  python app.py")
                print("\nOr test the database connection:")
                print("  python test_db.py")
                return True
            else:
                print("\n✗ No tables were created. Please check the SQL file.")
                return False
                
    except Error as e:
        print(f"\n✗ Error connecting to MySQL: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure XAMPP is installed and running")
        print("2. Start MySQL service in XAMPP Control Panel")
        print("3. Check if port 3306 is not blocked")
        print("4. Verify MySQL username and password")
        return False
        
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("\n✓ MySQL connection closed")

def update_config_file():
    """Update config.py with user's database credentials"""
    print("\n" + "=" * 50)
    print("Update Configuration File")
    print("=" * 50)
    
    update = input("\nDo you want to update config.py with your settings? (y/n): ").strip().lower()
    
    if update == 'y':
        host = input("MySQL host (default: localhost): ").strip() or "localhost"
        port = input("MySQL port (default: 3306): ").strip() or "3306"
        user = input("MySQL user (default: root): ").strip() or "root"
        password = input("MySQL password: ").strip()
        
        config_content = f"""# =========================
# Database Configuration
# =========================
# Configure these settings for your XAMPP MySQL database

DB_CONFIG = {{
    'host': '{host}',
    'port': {port},
    'user': '{user}',
    'password': '{password}',
    'database': 'coconut_ai',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': True,
    'raise_on_warnings': True
}}

# Connection pool settings
POOL_CONFIG = {{
    'pool_name': 'coconut_pool',
    'pool_size': 5,
    'pool_reset_session': True
}}

# Database connection retry settings
RETRY_CONFIG = {{
    'max_retries': 3,
    'retry_delay': 2  # seconds
}}
"""
        
        with open('config.py', 'w') as f:
            f.write(config_content)
        
        print("\n✓ config.py updated successfully!")

if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 48 + "╗")
    print("║" + " " * 10 + "CocoNUT AI Database Setup" + " " * 13 + "║")
    print("╚" + "=" * 48 + "╝")
    print("\n")
    
    # Check if database.sql exists
    if not os.path.exists('database.sql'):
        print("✗ Error: database.sql not found!")
        print("Please make sure you're running this script from the project directory.")
        sys.exit(1)
    
    # Create database
    success = create_database()
    
    if success:
        # Update config file
        update_config_file()
        
        print("\n" + "=" * 50)
        print("Setup Complete!")
        print("=" * 50)
        print("\nNext steps:")
        print("1. Install Python dependencies: pip install -r requirements.txt")
        print("2. Run the application: python app.py")
        print("3. Open http://localhost:5000 in your browser")
        print("\n")
    else:
        print("\n✗ Setup failed. Please fix the errors and try again.")
        sys.exit(1)
