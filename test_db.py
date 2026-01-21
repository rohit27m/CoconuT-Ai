"""
Test Database Connection for CocoNUT AI

This script tests the database connection and displays information
about the connected database.
"""

from database import DatabaseConnection
import sys

def test_connection():
    """Test database connection and display info"""
    print("\n" + "=" * 50)
    print("Testing CocoNUT AI Database Connection")
    print("=" * 50 + "\n")
    
    # Test connection
    print("1. Testing connection...")
    if DatabaseConnection.test_connection():
        print("   ✓ Database connection successful!\n")
    else:
        print("   ✗ Database connection failed!")
        print("\nTroubleshooting:")
        print("1. Make sure XAMPP MySQL is running")
        print("2. Check config.py settings")
        print("3. Run setup_database.py if you haven't")
        return False
    
    # Get database info
    print("2. Getting database information...")
    try:
        # Get tables
        tables_query = "SHOW TABLES"
        tables = DatabaseConnection.execute_query(tables_query, fetch=True)
        
        if tables:
            print(f"   ✓ Found {len(tables)} tables:")
            for table in tables:
                table_name = list(table.values())[0]
                
                # Get row count for each table
                count_query = f"SELECT COUNT(*) as count FROM {table_name}"
                result = DatabaseConnection.execute_query(count_query, fetch=True)
                count = result[0]['count'] if result else 0
                
                print(f"     - {table_name}: {count} rows")
        else:
            print("   ⚠ No tables found. Run setup_database.py first.")
            return False
        
        print("\n3. Testing database operations...")
        
        # Test user creation
        from database import create_user, get_user_by_username
        
        test_username = "test_user"
        print(f"   - Creating test user '{test_username}'...")
        
        # Check if user exists
        existing_user = get_user_by_username(test_username)
        if existing_user:
            print(f"   ✓ Test user already exists (ID: {existing_user['user_id']})")
        else:
            user_id = create_user(test_username, "test@example.com")
            if user_id:
                print(f"   ✓ Test user created successfully (ID: {user_id})")
            else:
                print("   ✗ Failed to create test user")
                return False
        
        print("\n" + "=" * 50)
        print("Database Connection Test: PASSED")
        print("=" * 50 + "\n")
        
        print("Your database is ready to use!")
        print("You can now run: python app.py")
        print()
        
        return True
        
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
        return False

if __name__ == "__main__":
    try:
        success = test_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)
