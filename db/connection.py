import sqlite3

conn = sqlite3.connect('rental_manager.db', check_same_thread=False)

def init_db():
    local_cursor = conn.cursor()

    # Rooms
    local_cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            room_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rent INTEGER NOT NULL,
            status TEXT CHECK(status IN ('available', 'occupied')) DEFAULT 'available'
        )
    ''')

    # Tenants
    local_cursor.execute('''
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

    # Payments
    local_cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id INTEGER,
            amount INTEGER,
            due_date TEXT,
            paid_date TEXT,
            status TEXT CHECK(status IN ('paid', 'unpaid')),
            FOREIGN KEY (tenant_id) REFERENCES tenants (tenant_id)
        )
    ''')

    conn.commit()
