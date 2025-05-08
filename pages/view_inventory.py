import streamlit as st
import pandas as pd
from core.database import view_all_products
from core.utils import export_to_csv, export_to_excel, plot_inventory_distribution

def app():
    st.subheader("Inventory List")

    if st.button(" Refresh Inventory"):
        st.cache_data.clear()
        st.experimental_rerun()  # Refresh immediately

    df = view_all_products()

    search = st.text_input("Search by name or SKU")
    if search:
        df = df[df["name"].str.contains(search, case=False) | df["sku"].str.contains(search, case=False)]

    st.dataframe(df if not df.empty else pd.DataFrame(columns=["name", "sku", "quantity", "reorder_level", "price"]))

    if not df.empty:
        st.download_button("Download as CSV", export_to_csv(df), "inventory.csv", "text/csv")
        st.download_button("Export as Excel", export_to_excel(df), "inventory.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    low_stock = df[df["quantity"] <= df["reorder_level"]]
    st.subheader("Low Stock Summary")
    st.dataframe(low_stock)

    if not low_stock.empty:
        for _, row in low_stock.iterrows():
            st.warning(f"Low stock alert: {row['name']} (SKU: {row['sku']})")
    else:
        st.info("No low stock alerts at this time.")

    st.subheader("Inventory Distribution")
    fig = plot_inventory_distribution(df)
    st.pyplot(fig)
