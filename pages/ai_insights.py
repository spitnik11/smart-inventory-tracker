import streamlit as st
from core.database import view_all_products

def app():
    st.subheader("AI-Powered Inventory Insights")

    df = view_all_products()

    if df.empty:
        st.warning("Inventory is empty. Please add products to get insights.")
        return

    st.markdown("Generating insights based on current stock levels...")

    low_stock_items = df[df["quantity"] <= df["reorder_level"]]

    if not low_stock_items.empty:
        messages = []
        for _, row in low_stock_items.iterrows():
            messages.append(f"{row['name']} (SKU: {row['sku']}) is running low. Only {row['quantity']} left in stock.")
        insights = "\n\n".join(messages)
    else:
        insights = "No low stock alerts. Inventory levels are sufficient."

    st.text_area("Inventory Summary", insights, height=300)
