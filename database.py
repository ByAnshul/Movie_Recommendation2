import sqlite3

def initialize_db():
    # Connect to SQLite database
    conn = sqlite3.connect('movie_dashboard.db')
    cursor = conn.cursor()
    
    # Create table for users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize the database
if __name__ == "__main__":
    initialize_db()
    print("Database initialized successfully.")
