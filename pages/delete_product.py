import streamlit as st
from core.database import delete_product, view_all_products

def app():
    st.subheader("Delete a Product")
    df = view_all_products()

    if not df.empty:
        # Refresh inventory after deletion
        sku_list = df["sku"].tolist()
        selected_sku = st.selectbox("Select SKU to Delete", sku_list)

        if st.button("Delete Product"):
            delete_product(selected_sku)
            st.success(f"Deleted product with SKU: {selected_sku}")
            st.experimental_rerun()  # Reload the page to refresh SKU list
    else:
        st.info("No products available to delete.")
