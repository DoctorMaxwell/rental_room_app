import sqlite3

# Connect to SQLite (shared connection for Streamlit)
conn = sqlite3.connect('rental_manager.db', check_same_thread=False)
cursor = conn.cursor()

def init_db():
    # Create Rooms table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            room_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rent INTEGER NOT NULL,
            status TEXT CHECK(status IN ('available', 'occupied')) DEFAULT 'available'
        )
    ''')

    # Create Tenants table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tenants (
            tenant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            room_id INTEGER,
            checkin_date TEXT,
            checkout_date TEXT,
            FOREIGN KEY (room_id) REFERENCES rooms (room_id)
        )
    ''')

    conn.commit()
