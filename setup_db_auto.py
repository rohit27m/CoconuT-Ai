"""
Automated Database Setup for CocoNUT AI
Uses XAMPP default settings (localhost, root, no password)
"""

import mysql.connector
from mysql.connector import Error
import os

def read_sql_file(filepath):
    """Read SQL file and return queries"""
    with open(filepath, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    return sql_content

def create_database():
    """Create the database and tables"""
    print("\n" + "=" * 60)
    print("  CocoNUT AI - Automated Database Setup (XAMPP)")
    print("=" * 60)
    
    # XAMPP default settings
    host = "localhost"
    port = 3306
    user = "root"
    password = ""
    
    print(f"\nUsing XAMPP default settings:")
    print(f"  Host: {host}")
    print(f"  Port: {port}")
    print(f"  User: {user}")
    print(f"  Password: (empty)")
    
    print("\n" + "=" * 60)
    print("Connecting to MySQL...")
    print("=" * 60)
    
    connection = None
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )
        
        if connection.is_connected():
            print("✓ Successfully connected to MySQL server")
            cursor = connection.cursor()
            
            # Read SQL file
            sql_file = 'database.sql'
            
            if not os.path.exists(sql_file):
                print(f"\n✗ Error: {sql_file} not found!")
                return False
            
            print(f"✓ Found {sql_file}")
            print("\n" + "=" * 60)
            print("Creating database and tables...")
            print("=" * 60)
            
            # Read and execute SQL file
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # Remove comments and split by semicolon
            statements = []
            for line in sql_content.split('\n'):
                line = line.strip()
                if line and not line.startswith('--'):
                    statements.append(line)
            
            # Join and split by semicolon
            full_sql = ' '.join(statements)
            sql_commands = [cmd.strip() for cmd in full_sql.split(';') if cmd.strip()]
            
            executed = 0
            skipped = 0
            
            for command in sql_commands:
                # Skip DELIMITER commands and empty statements
                if 'DELIMITER' in command.upper() or not command:
                    continue
                
                # Skip stored procedures for now (they need special handling)
                if 'CREATE PROCEDURE' in command.upper():
                    skipped += 1
                    continue
                
                try:
                    cursor.execute(command)
                    connection.commit()
                    executed += 1
                    # Consume any results to avoid "Unread result" error
                    try:
                        cursor.fetchall()
                    except:
                        pass
                except Error as e:
                    error_msg = str(e).lower()
                    if "already exists" in error_msg or "duplicate" in error_msg:
                        pass  # Ignore duplicate errors
                    else:
                        print(f"Warning: {e}")
            
            print(f"✓ Successfully executed {executed} SQL statements")
            if skipped > 0:
                print(f"  (Skipped {skipped} stored procedures - not needed for basic operation)")
            
            # Close connection and reconnect for verification
            cursor.close()
            connection.close()
            
            # Verify tables
            print("\n" + "=" * 60)
            print("Verifying database...")
            print("=" * 60)
            
            # Reconnect to verify
            connection = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database='coconut_ai'
            )
            cursor = connection.cursor()
            
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print(f"\n✓ Database 'coconut_ai' created successfully!")
                print(f"✓ Created {len(tables)} tables:")
                for table in tables:
                    print(f"  - {table[0]}")
                
                print("\n" + "=" * 60)
                print("✅ Database setup complete!")
                print("=" * 60)
                print("\nYou can now run your application:")
                print("  python app.py")
                print("\nOr test the database:")
                print("  python test_db.py")
                return True
            else:
                print("\n✗ No tables were created.")
                return False
                
    except Error as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure XAMPP Control Panel is open")
        print("2. Start MySQL service (should be green)")
        print("3. Check if MySQL password is set (default is empty)")
        print("4. Try accessing: http://localhost/phpmyadmin")
        return False
        
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("\n✓ MySQL connection closed")

if __name__ == "__main__":
    success = create_database()
    
    if not success:
        print("\n" + "=" * 60)
        print("❌ Setup failed!")
        print("=" * 60)
        print("\nNeed help? Check:")
        print("  - XAMPP_GUIDE.md")
        print("  - DATABASE_README.md")
        exit(1)
