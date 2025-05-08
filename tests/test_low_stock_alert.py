from streamlit.testing.v1 import AppTest
from reset_utils import reset_inventory_db
import time

def test_low_stock_alert():
    reset_inventory_db()

    at = AppTest.from_file("app.py")
    at.run()

    # Step 1: Add a low-stock product
    menu_select = next(sb for sb in at.selectbox if sb.label == "Menu")
    menu_select.select("Add Product").run()
    at.run()

    sku = f"TP{int(time.time())}"
    at.text_input[0].input("Low Stock Item")
    at.text_input[1].input(sku)
    at.number_input[0].set_value(2)     # Quantity
    at.number_input[1].set_value(5)     # Reorder level (threshold)
    at.number_input[2].set_value(1.99)  # Price
    at.button[0].click().run()

    # Step 2: View Inventory
    menu_select = next(sb for sb in at.selectbox if sb.label == "Menu")
    menu_select.select("View Inventory").run()
    at.run()

    # Step 3: Check if a low stock warning is shown
    warnings = [el.value for el in at.warning]
    assert any("Low stock" in msg for msg in warnings)

