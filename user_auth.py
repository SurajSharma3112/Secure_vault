import bcrypt
import database


def register_user(username, password):

    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    connection = database.get_db_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        
        if cursor.fetchone():
            return False, "Username already exists."

        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

        cursor.execute(
            "INSERT INTO users (username, password_hash, failed_attempts, is_locked) VALUES (%s, %s, %s, %s)",
            (username, password_hash, 0, False),
        )
        connection.commit()

        return True, "Registration successful."

    except Exception as e:
        print("Register Error:", e)
        return False, "Registration failed."

    finally:
        cursor.close()
        connection.close()


def login_user(username, password):
    connection = database.get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            return False, "Invalid username or password."

        if user["is_locked"]:
            return False, "Account locked due to multiple failed attempts."

        if bcrypt.checkpw(
            password.encode("utf-8"), user["password_hash"].encode("utf-8")
        ):

            cursor.execute(
                "UPDATE users SET failed_attempts = 0 WHERE id = %s", (user["id"],)
            )
            connection.commit()

            return True, user["id"]

        else:

            current_attempts = user["failed_attempts"] or 0
            new_attempts = current_attempts + 1

            is_locked = True if new_attempts >= 3 else False

            cursor.execute(
                "UPDATE users SET failed_attempts = %s, is_locked = %s WHERE id = %s",
                (new_attempts, is_locked, user["id"]),
            )
            connection.commit()

            return False, "Invalid username or password."

    except Exception as e:
        print("Login Error:", e)
        return False, "Login failed."

    finally:
        cursor.close()
        connection.close()
