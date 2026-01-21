import mysql.connector
from mysql.connector import pooling, Error
import time
from config import DB_CONFIG, POOL_CONFIG, RETRY_CONFIG
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """
    Database connection manager for CocoNUT AI
    Handles MySQL connections with connection pooling and error handling
    """
    
    _connection_pool = None
    
    @classmethod
    def initialize_pool(cls):
        """Initialize the connection pool"""
        try:
            if cls._connection_pool is None:
                cls._connection_pool = pooling.MySQLConnectionPool(
                    pool_name=POOL_CONFIG['pool_name'],
                    pool_size=POOL_CONFIG['pool_size'],
                    pool_reset_session=POOL_CONFIG['pool_reset_session'],
                    **DB_CONFIG
                )
                logger.info("Database connection pool initialized successfully")
            return True
        except Error as e:
            logger.error(f"Error initializing connection pool: {e}")
            return False
    
    @classmethod
    def get_connection(cls):
        """
        Get a connection from the pool with retry logic
        Returns: database connection or None
        """
        if cls._connection_pool is None:
            if not cls.initialize_pool():
                logger.error("Connection pool is not available")
                return None
        
        # Double-check pool is available after initialization attempt
        if cls._connection_pool is None:
            logger.error("Failed to initialize connection pool")
            return None
        
        for attempt in range(RETRY_CONFIG['max_retries']):
            try:
                connection = cls._connection_pool.get_connection()
                if connection.is_connected():
                    logger.debug("Database connection obtained successfully")
                    return connection
            except Error as e:
                logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < RETRY_CONFIG['max_retries'] - 1:
                    time.sleep(RETRY_CONFIG['retry_delay'])
                else:
                    logger.error("Failed to get database connection after all retries")
        
        return None
    
    @classmethod
    def execute_query(cls, query, params=None, fetch=False):
        """
        Execute a query with automatic connection handling
        
        Args:
            query: SQL query string
            params: Query parameters (tuple or dict)
            fetch: Whether to fetch results (True for SELECT queries)
        
        Returns:
            For SELECT: list of results
            For INSERT: last inserted ID
            For UPDATE/DELETE: number of affected rows
        """
        connection = None
        cursor = None
        
        try:
            connection = cls.get_connection()
            if connection is None:
                return None
            
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                results = cursor.fetchall()
                return results
            else:
                connection.commit()
                if query.strip().upper().startswith('INSERT'):
                    return cursor.lastrowid
                else:
                    return cursor.rowcount
                    
        except Error as e:
            logger.error(f"Database query error: {e}")
            if connection:
                connection.rollback()
            return None
            
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @classmethod
    def execute_many(cls, query, data_list):
        """
        Execute multiple queries at once (bulk insert/update)
        
        Args:
            query: SQL query string with placeholders
            data_list: List of tuples containing data
        
        Returns:
            Number of affected rows or None on error
        """
        connection = None
        cursor = None
        
        try:
            connection = cls.get_connection()
            if connection is None:
                return None
            
            cursor = connection.cursor()
            cursor.executemany(query, data_list)
            connection.commit()
            return cursor.rowcount
            
        except Error as e:
            logger.error(f"Bulk query error: {e}")
            if connection:
                connection.rollback()
            return None
            
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @classmethod
    def call_procedure(cls, procedure_name, args=None):
        """
        Call a stored procedure
        
        Args:
            procedure_name: Name of the stored procedure
            args: Tuple of arguments
        
        Returns:
            Results from the procedure
        """
        connection = None
        cursor = None
        
        try:
            connection = cls.get_connection()
            if connection is None:
                return None
            
            cursor = connection.cursor(dictionary=True)
            cursor.callproc(procedure_name, args or ())
            
            # Fetch results if any
            results = []
            for result in cursor.stored_results():
                results.extend(result.fetchall())
            
            connection.commit()
            return results
            
        except Error as e:
            logger.error(f"Procedure call error: {e}")
            if connection:
                connection.rollback()
            return None
            
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @classmethod
    def test_connection(cls):
        """
        Test database connection
        Returns: True if connection successful, False otherwise
        """
        connection = None
        try:
            connection = cls.get_connection()
            if connection and connection.is_connected():
                db_info = connection.get_server_info()
                logger.info(f"Successfully connected to MySQL Server version {db_info}")
                
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE();")
                record = cursor.fetchone()
                logger.info(f"Connected to database: {record[0]}")
                cursor.close()
                
                return True
            else:
                logger.error("Failed to connect to database")
                return False
                
        except Error as e:
            logger.error(f"Connection test failed: {e}")
            return False
            
        finally:
            if connection and connection.is_connected():
                connection.close()


# =========================
# Database Helper Functions
# =========================

def create_user(username, email=None, preferences=None):
    """Create a new user"""
    query = """
        INSERT INTO users (username, email, preferences)
        VALUES (%s, %s, %s)
    """
    import json
    prefs_json = json.dumps(preferences) if preferences else None
    return DatabaseConnection.execute_query(query, (username, email, prefs_json))


def get_user_by_username(username):
    """Get user by username"""
    query = "SELECT * FROM users WHERE username = %s"
    results = DatabaseConnection.execute_query(query, (username,), fetch=True)
    return results[0] if results else None


def start_conversation(user_id, session_id):
    """Start a new conversation"""
    query = """
        INSERT INTO conversations (user_id, session_id)
        VALUES (%s, %s)
    """
    return DatabaseConnection.execute_query(query, (user_id, session_id))


def log_message(conversation_id, user_id, message_type, message_text, mood=None, confidence=None):
    """Log a message to the database"""
    query = """
        INSERT INTO messages (conversation_id, user_id, message_type, message_text, detected_mood, mood_confidence)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    return DatabaseConnection.execute_query(
        query, 
        (conversation_id, user_id, message_type, message_text, mood, confidence)
    )


def log_mood(user_id, mood, confidence, context=None):
    """Log user mood"""
    query = """
        INSERT INTO mood_history (user_id, mood, confidence, context)
        VALUES (%s, %s, %s, %s)
    """
    return DatabaseConnection.execute_query(query, (user_id, mood, confidence, context))


def get_conversation_history(user_id, limit=50):
    """Get recent conversation history"""
    query = """
        SELECT m.*, c.session_id
        FROM messages m
        JOIN conversations c ON m.conversation_id = c.conversation_id
        WHERE m.user_id = %s
        ORDER BY m.timestamp DESC
        LIMIT %s
    """
    return DatabaseConnection.execute_query(query, (user_id, limit), fetch=True)


def get_mood_trends(user_id, days=7):
    """Get mood trends for a user"""
    query = """
        SELECT mood, COUNT(*) as count, AVG(confidence) as avg_confidence
        FROM mood_history
        WHERE user_id = %s
        AND detected_at >= DATE_SUB(NOW(), INTERVAL %s DAY)
        GROUP BY mood
        ORDER BY count DESC
    """
    return DatabaseConnection.execute_query(query, (user_id, days), fetch=True)


def update_ai_knowledge(topic, pattern, response, was_successful):
    """Update AI knowledge base"""
    query = """
        INSERT INTO ai_knowledge (topic, pattern, response, usage_count, success_rate)
        VALUES (%s, %s, %s, 1, %s)
        ON DUPLICATE KEY UPDATE
            usage_count = usage_count + 1,
            success_rate = IF(%s, 
                (success_rate * usage_count + 1) / (usage_count + 1),
                (success_rate * usage_count) / (usage_count + 1))
    """
    success = 1.0 if was_successful else 0.0
    return DatabaseConnection.execute_query(query, (topic, pattern, response, success, was_successful))


def get_knowledge_by_topic(topic):
    """Get knowledge patterns by topic"""
    query = """
        SELECT * FROM ai_knowledge
        WHERE topic = %s
        ORDER BY success_rate DESC, usage_count DESC
    """
    return DatabaseConnection.execute_query(query, (topic,), fetch=True)


# Initialize connection pool on module import
DatabaseConnection.initialize_pool()
