import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('inventory.db')
c = conn.cursor()

# Create the products table
c.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    sku TEXT UNIQUE NOT NULL,
    quantity INTEGER NOT NULL,
    reorder_level INTEGER NOT NULL,
    price REAL NOT NULL
)
''')

conn.commit()
conn.close()