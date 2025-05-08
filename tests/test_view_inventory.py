from streamlit.testing.v1 import AppTest
from reset_utils import reset_inventory_db
import time

def test_view_inventory_contains_added_product():
    reset_inventory_db()

    at = AppTest.from_file("app.py")
    at.run()

    # Step 1: Add a unique product
    at.selectbox[0].select("Add Product").run()
    time.sleep(1)

    unique_sku = f"TP{int(time.time())}"
    at.text_input[0].input("Test Product")
    at.text_input[1].input(unique_sku)
    at.number_input[0].set_value(10)
    at.number_input[1].set_value(5)
    at.number_input[2].set_value(9.99)
    at.button[0].click().run()

    # Step 2: Switch to "View Inventory"
    at.selectbox[0].select("View Inventory").run()
    time.sleep(1)

    # Step 3: Check that the product appears in the inventory table
    inventory_table = at.dataframe[0].value
    assert "Test Product" in inventory_table["name"].values
    assert unique_sku in inventory_table["sku"].values
