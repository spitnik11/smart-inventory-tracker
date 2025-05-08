import sqlite3
import pandas as pd
from core.config import DB_PATH
import os


def get_connection():
    """
    Establishes and returns a SQLite DB connection.
    """
    return sqlite3.connect(DB_PATH)

def ensure_db_initialized():
    """
    Ensures the products table exists.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                sku TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                reorder_level INTEGER NOT NULL,
                price REAL NOT NULL
            )
        """)
        conn.commit()

def view_all_products():
    """
    Fetches all product entries from the database.

    Returns:
        pd.DataFrame: Product list or empty dataframe on failure.
    """
    try:
        with get_connection() as conn:
            return pd.read_sql_query("SELECT * FROM products", conn)
    except sqlite3.Error as e:
        print(f"[DB ERROR] {e}")
        return pd.DataFrame()

def add_product(name, sku, quantity, reorder_level, price):
    """
    Inserts a new product into the database.

    Returns:
        tuple(bool, str): Success flag and message.
    """
    if not name or not sku or quantity < 0 or price < 0:
        return False, "Invalid input: fields must not be empty and numbers must be non-negative."

    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO products (name, sku, quantity, reorder_level, price)
                VALUES (?, ?, ?, ?, ?)
            """, (name, sku, quantity, reorder_level, price))
            conn.commit()
        return True, "Product added successfully."
    except sqlite3.IntegrityError:
        return False, f"A product with SKU '{sku}' already exists."
    except sqlite3.Error as e:
        return False, f"Database error: {e}"

def update_quantity(sku, quantity):
    """
    Modifies the quantity of a product.

    Args:
        sku (str): SKU identifier.
        quantity (int): Amount to add (can be negative).
    """
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("UPDATE products SET quantity = quantity + ? WHERE sku = ?", (quantity, sku))
            conn.commit()
    except sqlite3.Error as e:
        print(f"[DB ERROR] Failed to update quantity: {e}")

def delete_product(sku):
    """
    Deletes a product by SKU.

    Args:
        sku (str): SKU of the product to delete.
    """
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM products WHERE sku = ?", (sku,))
            conn.commit()
    except sqlite3.Error as e:
        print(f"[DB ERROR] Failed to delete product: {e}")

def reset_inventory_db():
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sku TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            reorder_level INTEGER NOT NULL,
            price REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()
