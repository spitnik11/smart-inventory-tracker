import streamlit as st
from pages import view_inventory, add_product, update_quantity, delete_product, ai_insights

st.set_page_config(layout="wide")
st.title("Smart Inventory Tracker")

from core.database import ensure_db_initialized
ensure_db_initialized()

if st.sidebar.button(" Reset Inventory DB"):
    from core.database import reset_inventory_db
    reset_inventory_db()
    st.sidebar.success("Database reset complete.")

# Sidebar navigation
PAGES = {
    "View Inventory": view_inventory,
    "Add Product": add_product,
    "Update Quantity": update_quantity,
    "Delete Product": delete_product,
    "AI Insights": ai_insights  
}

choice = st.sidebar.radio(" Menu", list(PAGES.keys()))
PAGES[choice].app()
