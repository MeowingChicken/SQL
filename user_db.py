import sqlite3

# Connect to database
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT UNIQUE NOT NULL,
    Password TEXT NOT NULL
)
""")
conn.commit()


def create_user(username, password):
    """
    Add a new user to the database.

    Parameters:
        username (str)
        password (str)

    Returns:
        bool: True if successful, False if username exists
    """
    try:
        cursor.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def verify_user(username, password):
    """
    Check if username/password combination exists.

    Parameters:
        username (str)
        password (str)

    Returns:
        bool
    """
    cursor.execute("SELECT 1 FROM Users WHERE Username=? AND Password=?", (username, password))
    return cursor.fetchone() is not None
