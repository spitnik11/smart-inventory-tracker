import sqlite3
import time

def reset_inventory_db(retries=5, delay=1):
    for attempt in range(retries):
        try:
            conn = sqlite3.connect("inventory.db", timeout=1)
            c = conn.cursor()
            c.execute("DELETE FROM products")
            conn.commit()
            conn.close()
            return
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower():
                time.sleep(delay)
            else:
                raise
    raise RuntimeError("Database remained locked after several attempts")