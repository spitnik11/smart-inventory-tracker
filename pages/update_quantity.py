import streamlit as st
from core.database import update_quantity, view_all_products

def app():
    st.subheader("Update Product Quantity")

    df = view_all_products()
    if df.empty:
        st.warning("No products found in the inventory.")
        return

    sku_list = df["sku"].tolist()
    selected_sku = st.selectbox("Select SKU", sku_list, key="select_sku")
    quantity = st.number_input("Quantity to Add/Subtract", min_value=-1000, max_value=1000, key="adjust_qty")

    if st.button("Update Quantity"):
        update_quantity(selected_sku, quantity)
        st.success(f"Updated quantity for SKU: {selected_sku} by {quantity}")
        st.experimental_rerun()  # Refresh to show updated values
