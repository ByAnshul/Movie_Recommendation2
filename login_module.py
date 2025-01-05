import streamlit as st
import sqlite3
import bcrypt

# Hash passwords using bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

# Authenticate user
def authenticate_user(username, password):
    conn = sqlite3.connect("movie_dashboard.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode(), user[1]):
        return user[0]  # Return username if authenticated
    return None

# Register user
def register_user(username, email, password):
    conn = sqlite3.connect("movie_dashboard.db")
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                       (username, email, hashed_password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# Login or Register UI
def login_ui():
    st.title("User Authentication")
    tab1, tab2 = st.tabs(["Login", "Register"])

    # Login Tab
    with tab1:
        st.subheader("Login")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # Create two columns for buttons
        col1, col2 = st.columns([1,20])

        with col1:
            if st.button("Login"):
                user = authenticate_user(username, password)
                if user:
                    st.success(f"Welcome back, {user}!")
                    st.session_state.logged_in = True
                    st.session_state.username = user
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

        with col2:
            if st.button("Skip"):
                st.session_state.logged_in = True
                st.session_state.username = "Guest"
                st.rerun()


    # Register Tab
    with tab2:
        st.subheader("Register")
        reg_user = st.text_input("Choose a Username")
        reg_email = st.text_input("Enter your Email")
        reg_pass = st.text_input("Choose a Password", type="password")
        if st.button("Register"):
            if register_user(reg_user, reg_email, reg_pass):
                st.success("Registration successful! Please log in.")
            else:
                st.error("Username or email already exists.")

    # Skip Tab

        

# Check login status
def check_login():
    return st.session_state.get("logged_in", False)
