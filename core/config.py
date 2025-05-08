# core/config.py
import os

DB_PATH = os.getenv("DB_PATH", "inventory.db")
REORDER_THRESHOLD_DEFAULT = 5