import streamlit as st
from pages import rooms, tenants
from db.connection import init_db
# TEMPORARY DEBUG TOOL (you can delete later)
import pandas as pd
from db.connection import conn
debug_df = pd.read_sql_query("SELECT room_id, name, status FROM rooms", conn)
st.sidebar.markdown("### Debug: Room Status Table")
st.sidebar.dataframe(debug_df)

# Initialize DB
init_db()

# Sidebar menu
st.sidebar.title("Rental Room Manager")
menu = st.sidebar.radio("Go to", ["Rooms", "Tenants"])

# Route to pages
if menu == "Rooms":
    rooms.show()
elif menu == "Tenants":
    tenants.show()
