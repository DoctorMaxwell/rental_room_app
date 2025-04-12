import streamlit as st
import pandas as pd
from db.connection import conn, cursor
from datetime import datetime

def show():
    st.title("Payment Management")

    # Select tenant
    df_tenants = pd.read_sql_query("SELECT tenant_id, name FROM tenants", conn)

    if df_tenants.empty:
        st.warning("No tenants found.")
        return

    selected_tenant_name = st.selectbox("Select tenant", df_tenants["name"])
    tenant_id = df_tenants[df_tenants["name"] == selected_tenant_name]["tenant_id"].values[0]

    # Payment input
    amount = st.number_input("Payment amount", min_value=0, step=50000)
    due_date = st.date_input("Due date")
    paid_date = st.date_input("Paid date (optional)", value=datetime.today())
    status = st.selectbox("Status", ["paid", "unpaid"])

    if st.button("Add Payment"):
        cursor.execute('''
            INSERT INTO payments (tenant_id, amount, due_date, paid_date, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (tenant_id, amount, due_date.strftime("%Y-%m-%d"), paid_date.strftime("%Y-%m-%d"), status))
        conn.commit()
        st.success("Payment record added.")

    # Show all payments
    st.subheader("Payment Records")
    df_payments = pd.read_sql_query('''
        SELECT payments.payment_id, tenants.name AS tenant_name, amount, due_date, paid_date, status
        FROM payments
        LEFT JOIN tenants ON payments.tenant_id = tenants.tenant_id
    ''', conn)
    st.dataframe(df_payments)
