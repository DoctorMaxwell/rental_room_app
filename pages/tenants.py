import streamlit as st
import pandas as pd
from db.connection import conn, cursor
from datetime import datetime

def show():
    st.title("Tenant Management")

    # Register Tenant Section
    st.subheader("Register New Tenant")
    tenant_name = st.text_input("Tenant name")
    tenant_phone = st.text_input("Phone number")

    # Load available rooms with both name and ID
    available_rooms = pd.read_sql_query(
        "SELECT room_id, name FROM rooms WHERE status = 'available'", conn
    )

    if not available_rooms.empty:
        # Show dropdown with room name, but keep track of room_id
        room_option = st.selectbox(
            "Assign to room",
            available_rooms.apply(lambda row: f"{row['name']} (ID: {row['room_id']})", axis=1)
        )

        if st.button("Register Tenant") and tenant_name:
            try:
                checkin_date = datetime.now().strftime("%Y-%m-%d")

                # Parse room_id from selection
                room_id = int(room_option.split("ID:")[1].replace(")", "").strip())
                selected_room_name = available_rooms[available_rooms["room_id"] == room_id]["name"].values[0]

                # Insert tenant
                cursor.execute('''
                    INSERT INTO tenants (name, phone, room_id, checkin_date)
                    VALUES (?, ?, ?, ?)
                ''', (tenant_name, tenant_phone, room_id, checkin_date))

                # Update room status
                cursor.execute("UPDATE rooms SET status = 'occupied' WHERE room_id = ?", (room_id,))
                conn.commit()

                st.success(f"Tenant '{tenant_name}' assigned to room '{selected_room_name}'.")

            except Exception as e:
                st.error(f"Failed to register tenant: {e}")
    else:
        st.warning("No available rooms.")

    # Tenant List
    st.subheader("Tenant List")
    df_tenants = pd.read_sql_query('''
        SELECT tenants.name, tenants.phone, tenants.checkin_date, tenants.checkout_date,
               rooms.name AS room_name
        FROM tenants
        LEFT JOIN rooms ON tenants.room_id = rooms.room_id
    ''', conn)
    st.dataframe(df_tenants)
