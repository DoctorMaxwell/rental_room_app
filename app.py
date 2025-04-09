import streamlit as st
import sqlite3
import pandas as pd

# Connect to SQLite
conn = sqlite3.connect('rental_manager.db', check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS rooms (
        room_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        rent INTEGER NOT NULL,
        status TEXT CHECK(status IN ('available', 'occupied')) DEFAULT 'available'
    )
''')
conn.commit()

st.title("Room Management")

# Add new room
st.subheader("Add New Room")
room_name = st.text_input("Room name")
room_rent = st.number_input("Monthly rent", min_value=0)
room_status = st.selectbox("Status", ['available', 'occupied'])
if st.button("Add Room"):
    cursor.execute("INSERT INTO rooms (name, rent, status) VALUES (?, ?, ?)",
                   (room_name, room_rent, room_status))
    conn.commit()
    st.success(f"Room '{room_name}' added.")

# View all rooms
st.subheader("Room List")
df = pd.read_sql_query("SELECT * FROM rooms", conn)
st.dataframe(df)
