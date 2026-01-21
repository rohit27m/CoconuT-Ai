-- =========================
-- CocoNUT AI Database Schema
-- Compatible with MySQL/MariaDB (XAMPP)
-- =========================

-- Create database
CREATE DATABASE IF NOT EXISTS coconut_ai 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE coconut_ai;

-- =========================
-- Users Table
-- =========================
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    preferences JSON,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================
-- Conversations Table
-- =========================
CREATE TABLE IF NOT EXISTS conversations (
    conversation_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_id VARCHAR(255) NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP NULL,
    total_messages INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_session (user_id, session_id),
    INDEX idx_started_at (started_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================
-- Messages Table
-- =========================
CREATE TABLE IF NOT EXISTS messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id INT NOT NULL,
    user_id INT NOT NULL,
    message_type ENUM('user', 'ai') NOT NULL,
    message_text TEXT NOT NULL,
    detected_mood VARCHAR(50),
    mood_confidence FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_conversation (conversation_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_mood (detected_mood)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================
-- Mood History Table
-- =========================
CREATE TABLE IF NOT EXISTS mood_history (
    mood_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    mood VARCHAR(50) NOT NULL,
    confidence FLOAT NOT NULL,
    context TEXT,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_mood (user_id, mood),
    INDEX idx_detected_at (detected_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================
-- AI Knowledge Base Table
-- =========================
CREATE TABLE IF NOT EXISTS ai_knowledge (
    knowledge_id INT AUTO_INCREMENT PRIMARY KEY,
    topic VARCHAR(255) NOT NULL,
    pattern TEXT NOT NULL,
    response TEXT NOT NULL,
    usage_count INT DEFAULT 0,
    success_rate FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_topic (topic),
    INDEX idx_success_rate (success_rate)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================
-- User Preferences Table
-- =========================
CREATE TABLE IF NOT EXISTS user_preferences (
    preference_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    preference_key VARCHAR(100) NOT NULL,
    preference_value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_preference (user_id, preference_key),
    INDEX idx_user_key (user_id, preference_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================
-- Response Feedback Table
-- =========================
CREATE TABLE IF NOT EXISTS response_feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    message_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    feedback_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (message_id) REFERENCES messages(message_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_message (message_id),
    INDEX idx_rating (rating)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================
-- Word Associations Table
-- =========================
CREATE TABLE IF NOT EXISTS word_associations (
    association_id INT AUTO_INCREMENT PRIMARY KEY,
    word VARCHAR(100) NOT NULL,
    associated_word VARCHAR(100) NOT NULL,
    strength FLOAT DEFAULT 1.0,
    context VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_word (word),
    INDEX idx_strength (strength)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================
-- Session Analytics Table
-- =========================
CREATE TABLE IF NOT EXISTS session_analytics (
    analytics_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_id VARCHAR(255) NOT NULL,
    session_date DATE NOT NULL,
    total_messages INT DEFAULT 0,
    avg_response_time FLOAT,
    dominant_mood VARCHAR(50),
    interaction_quality FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, session_date),
    INDEX idx_session (session_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================
-- Learning Patterns Table
-- =========================
CREATE TABLE IF NOT EXISTS learning_patterns (
    pattern_id INT AUTO_INCREMENT PRIMARY KEY,
    pattern_type VARCHAR(50) NOT NULL,
    input_pattern TEXT NOT NULL,
    learned_response TEXT NOT NULL,
    success_count INT DEFAULT 0,
    failure_count INT DEFAULT 0,
    last_used TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_pattern_type (pattern_type),
    INDEX idx_success_count (success_count)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================
-- Insert Default Data
-- =========================

-- Insert a default user for testing
INSERT INTO users (username, email, preferences) 
VALUES ('guest', 'guest@coconutai.local', '{"conversation_style": "friendly", "interests": []}')
ON DUPLICATE KEY UPDATE username=username;

-- Insert default mood responses
INSERT INTO ai_knowledge (topic, pattern, response, usage_count, success_rate) 
VALUES 
('greeting', 'hello|hi|hey', 'Hello! How are you feeling today?', 0, 0.0),
('farewell', 'bye|goodbye|see you', 'Goodbye! Take care!', 0, 0.0),
('thanks', 'thank|thanks', 'You\'re welcome! Happy to help!', 0, 0.0),
('help', 'help|assist|support', 'I\'m here to help! What do you need?', 0, 0.0),
('mood_inquiry', 'how are you|what\'s up', 'I\'m doing great! How about you?', 0, 0.0)
ON DUPLICATE KEY UPDATE topic=topic;

-- =========================
-- Views for Analytics
-- =========================

-- User activity summary view
CREATE OR REPLACE VIEW user_activity_summary AS
SELECT 
    u.user_id,
    u.username,
    COUNT(DISTINCT c.conversation_id) as total_conversations,
    COUNT(m.message_id) as total_messages,
    u.last_active,
    DATEDIFF(NOW(), u.created_at) as days_active
FROM users u
LEFT JOIN conversations c ON u.user_id = c.user_id
LEFT JOIN messages m ON u.user_id = m.user_id
GROUP BY u.user_id, u.username, u.last_active, u.created_at;

-- Mood trends view
CREATE OR REPLACE VIEW mood_trends AS
SELECT 
    user_id,
    mood,
    COUNT(*) as frequency,
    AVG(confidence) as avg_confidence,
    DATE(detected_at) as mood_date
FROM mood_history
GROUP BY user_id, mood, DATE(detected_at);

-- Knowledge base performance view
CREATE OR REPLACE VIEW knowledge_performance AS
SELECT 
    topic,
    COUNT(*) as total_patterns,
    AVG(success_rate) as avg_success_rate,
    SUM(usage_count) as total_usage
FROM ai_knowledge
GROUP BY topic
ORDER BY total_usage DESC;

-- =========================
-- Stored Procedures
-- =========================

DELIMITER //

-- Procedure to log a conversation message
CREATE PROCEDURE log_message(
    IN p_conversation_id INT,
    IN p_user_id INT,
    IN p_message_type ENUM('user', 'ai'),
    IN p_message_text TEXT,
    IN p_detected_mood VARCHAR(50),
    IN p_mood_confidence FLOAT
)
BEGIN
    INSERT INTO messages (conversation_id, user_id, message_type, message_text, detected_mood, mood_confidence)
    VALUES (p_conversation_id, p_user_id, p_message_type, p_message_text, p_detected_mood, p_mood_confidence);
    
    -- Update conversation message count
    UPDATE conversations 
    SET total_messages = total_messages + 1 
    WHERE conversation_id = p_conversation_id;
    
    -- Log mood if detected
    IF p_detected_mood IS NOT NULL THEN
        INSERT INTO mood_history (user_id, mood, confidence, context)
        VALUES (p_user_id, p_detected_mood, p_mood_confidence, SUBSTRING(p_message_text, 1, 255));
    END IF;
END //

-- Procedure to start a new conversation
CREATE PROCEDURE start_conversation(
    IN p_user_id INT,
    IN p_session_id VARCHAR(255),
    OUT p_conversation_id INT
)
BEGIN
    INSERT INTO conversations (user_id, session_id)
    VALUES (p_user_id, p_session_id);
    
    SET p_conversation_id = LAST_INSERT_ID();
END //

-- Procedure to update AI knowledge
CREATE PROCEDURE update_knowledge(
    IN p_topic VARCHAR(255),
    IN p_pattern TEXT,
    IN p_response TEXT,
    IN p_was_successful BOOLEAN
)
BEGIN
    DECLARE v_knowledge_id INT;
    
    SELECT knowledge_id INTO v_knowledge_id
    FROM ai_knowledge
    WHERE topic = p_topic AND pattern = p_pattern
    LIMIT 1;
    
    IF v_knowledge_id IS NOT NULL THEN
        UPDATE ai_knowledge
        SET usage_count = usage_count + 1,
            success_rate = IF(p_was_successful, 
                (success_rate * usage_count + 1) / (usage_count + 1),
                (success_rate * usage_count) / (usage_count + 1))
        WHERE knowledge_id = v_knowledge_id;
    ELSE
        INSERT INTO ai_knowledge (topic, pattern, response, usage_count, success_rate)
        VALUES (p_topic, p_pattern, p_response, 1, IF(p_was_successful, 1.0, 0.0));
    END IF;
END //

DELIMITER ;

-- =========================
-- Indexes for Performance
-- =========================

-- Additional performance indexes
CREATE INDEX idx_message_type ON messages(message_type);
CREATE INDEX idx_conversation_timestamp ON messages(conversation_id, timestamp);
CREATE INDEX idx_user_timestamp ON messages(user_id, timestamp);

-- =========================
-- Database Setup Complete
-- =========================

SELECT 'Database schema created successfully!' AS status;
