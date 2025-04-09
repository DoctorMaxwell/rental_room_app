import streamlit as st
from pages import rooms, tenants
from db.connection import init_db

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
