from streamlit.testing.v1 import AppTest
from reset_utils import reset_inventory_db
import time

def test_excel_export_button():
    from core.database import reset_inventory_db
    reset_inventory_db()

    at = AppTest.from_file("app.py")
    at.run()

    # Navigate to Add Product
    menu = next(sb for sb in at.selectbox if sb.label == "Menu")
    menu.select("Add Product").run()
    at.run()

    sku = f"XL{int(time.time())}"
    at.text_input[0].input("Excel Export Test Product")
    at.text_input[1].input(sku)
    at.number_input[0].set_value(10)
    at.number_input[1].set_value(5)
    at.number_input[2].set_value(19.99)
    at.button[0].click().run()

    # View Inventory
    menu = next(sb for sb in at.selectbox if sb.label == "Menu")
    menu.select("View Inventory").run()
    at.run()

    # Confirm product added
    df = at.dataframe[0].value
    assert not df.empty, "Expected inventory to have at least one product"

    #  Check download button labels
    labels = [btn.label.lower() for btn in at.download_button]
    assert any("excel" in label for label in labels), "Excel export button not found"
