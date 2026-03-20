import mysql.connector



def get_db_connection():
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "secure_vault"
    )
    return connection

def setup_database():
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = ""
    )
    cursor = connection.cursor
    cursor.execute("CREATE DATABASE IF NOT EXISTS secure_vault")  
    cursor.execute("USE secure_vault")
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS user(
              id INT AUTO_INCREMENT PRIMARY KEY,
              user_name VARCHAR(255) UNIQUE NOT NULL,
              password VARCHAR(255) NOT NULL,
              failed_attempts INT DEFAULT 0,
              is_locked BOOLEAN DEFAULT FALSE
            )"""
    )
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_metadata(
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                original_filename VARCHAR(255) NOT NULL,
                encrypted_filename VARCHAR(255) NOT NULL,
                file_size INT,
                upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                FOREIGN KEY(user_id) REFERENCES user(id)
            )"""
    ) 

    connection.commit
    cursor.close
    connection.close
    print("database setup complete")
 

if __name__ == "__main__":
    setup_database        