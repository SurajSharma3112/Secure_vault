import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="3112",
        database="pysecurevault"
    )
    return connection

def setup_database():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="3112"
    )
    cursor = connection.cursor()
    
    cursor.execute("CREATE DATABASE IF NOT EXISTS pysecurevault")
    cursor.execute("USE pysecurevault")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            failed_attempts INT DEFAULT 0,
            is_locked BOOLEAN DEFAULT FALSE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS file_metadata (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            original_filename VARCHAR(255) NOT NULL,
            encrypted_filename VARCHAR(255) NOT NULL,
            file_size INT,
            upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    connection.commit()
    cursor.close()
    connection.close()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()