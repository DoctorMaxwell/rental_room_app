import streamlit as st
from modules import rooms, tenants
from db.connection import init_db, conn
import pandas as pd

# Always initialize DB
init_db()

# Sidebar navigation
st.sidebar.title("Rental Room Manager")
menu = st.sidebar.radio("Go to", ["Rooms", "Tenants", "Payments"])

# DEBUG: Show current room status
try:
    debug_df = pd.read_sql_query("SELECT room_id, name, status FROM rooms", conn)
    st.sidebar.markdown("### Debug: Room Status")
    st.sidebar.dataframe(debug_df)
except Exception as e:
    st.sidebar.error(f"DEBUG ERROR: {e}")

# Routing
if menu == "Rooms":
    rooms.show()
elif menu == "Tenants":
    tenants.show()
elif menu == "Payments":
    payments.show()
