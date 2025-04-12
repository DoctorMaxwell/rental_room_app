import streamlit as st
import pandas as pd
from db.connection import conn

cursor = conn.cursor()

def show():
    st.title("Room Management")

    # Add Room Section
    st.subheader("Add New Room")
    room_name = st.text_input("Room name")
    room_rent = st.number_input("Monthly rent", min_value=0, step=50000, value=500000)
    room_status = st.selectbox("Status", ['available', 'occupied'])

    if st.button("Add Room"):
        if room_name:
            cursor.execute("INSERT INTO rooms (name, rent, status) VALUES (?, ?, ?)",
                           (room_name, room_rent, room_status))
            conn.commit()
            st.success(f"Room '{room_name}' added.")
        else:
            st.warning("Room name is required.")

    # Room List
    st.subheader("Room List")
    df_rooms = pd.read_sql_query("SELECT * FROM rooms", conn)
    st.dataframe(df_rooms)
