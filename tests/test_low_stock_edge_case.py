from streamlit.testing.v1 import AppTest
from reset_utils import reset_inventory_db
import time

def test_low_stock_edge_case():
    reset_inventory_db()

    at = AppTest.from_file("app.py")
    at.run()

    # Step 1: Add product with quantity == reorder level
    menu_select = next(sb for sb in at.selectbox if sb.label == "Menu")
    menu_select.select("Add Product").run()
    at.run()

    sku = f"TP{int(time.time())}"
    at.text_input[0].input("EdgeCase Product")
    at.text_input[1].input(sku)
    at.number_input[0].set_value(5)  # quantity
    at.number_input[1].set_value(5)  # reorder level (equal)
    at.number_input[2].set_value(9.99)
    at.button[0].click().run()

    # Step 2: Go to View Inventory
    menu_select = next(sb for sb in at.selectbox if sb.label == "Menu")
    menu_select.select("View Inventory").run()
    at.run()

    # Step 3: Check for warning about low stock
    warning_found = any(
        "low stock alert" in str(w.value).lower()
        for w in at.warning
    )

    assert warning_found, "Expected low stock warning for quantity == reorder level"