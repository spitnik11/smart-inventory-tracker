import streamlit as st
from core.database import add_product
import re

def is_valid_sku(sku: str) -> bool:
    return bool(re.match(r"^[\w-]+$", sku))

def app():
    st.subheader(" Add New Product")

    with st.form("add_product_form"):
        name = st.text_input("Product Name")
        sku = st.text_input("SKU (letters, numbers, dashes only)")
        quantity = st.number_input("Quantity", min_value=0)
        reorder_level = st.number_input("Reorder Level", min_value=0)
        price = st.number_input("Price", min_value=0.0, format="%.2f")

        submitted = st.form_submit_button("Add Product")

        if submitted:
            if not name or not is_valid_sku(sku):
                st.error("Please enter a valid product name and SKU.")
            else:
                success, message = add_product(name, sku, quantity, reorder_level, price)
                if success:
                    st.success(message)
                else:
                    st.error(message)
