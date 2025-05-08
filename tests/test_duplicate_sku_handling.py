import time
from streamlit.testing.v1 import AppTest
from reset_utils import reset_inventory_db

def test_duplicate_sku_handling():
    reset_inventory_db()

    at = AppTest.from_file("app.py")
    at.run()

    # Step 1: Navigate to "Add Product"
    menu_select = next(sb for sb in at.selectbox if sb.label == "Menu")
    menu_select.select("Add Product").run()
    at.run()

    # Use a unique SKU
    sku = f"TP{int(time.time())}"

    # First entry
    at.text_input[0].input("Original Product")
    at.text_input[1].input(sku)
    at.number_input[0].set_value(5)
    at.number_input[1].set_value(2)
    at.number_input[2].set_value(9.99)
    at.button[0].click().run()

    # Second entry with the same SKU
    at.text_input[0].input("Duplicate Product")
    at.text_input[1].input(sku)
    at.number_input[0].set_value(3)
    at.number_input[1].set_value(1)
    at.number_input[2].set_value(5.55)
    at.button[0].click().run()

    # Step 3: Confirm warning message shown
    warning_messages = [w.value.lower() for w in at.warning]
    assert any("already exists" in msg or "unique constraint" in msg for msg in warning_messages), \
        "Expected a warning for duplicate SKU"
