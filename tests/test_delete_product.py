from streamlit.testing.v1 import AppTest
from reset_utils import reset_inventory_db
import time

def test_delete_product():
    reset_inventory_db()

    at = AppTest.from_file("app.py")
    at.run()

    # Step 1: Add a product
    menu_select = next(sb for sb in at.selectbox if sb.label == "Menu")
    menu_select.select("Add Product").run()
    at.run()

    sku = f"TP{int(time.time())}"
    at.text_input[0].input("Delete Test")
    at.text_input[1].input(sku)
    at.number_input[0].set_value(5)
    at.number_input[1].set_value(1)
    at.number_input[2].set_value(9.99)
    at.button[0].click().run()

    # Step 2: Go to Delete Product
    menu_select = next(sb for sb in at.selectbox if sb.label == "Menu")
    menu_select.select("Delete Product").run()
    at.run()

    sku_select = next(sb for sb in at.selectbox if sb.label == "Select SKU to Delete")
    sku_select.select(sku).run()
    at.button[0].click().run()

    # Step 3: Verify it's gone
    menu_select = next(sb for sb in at.selectbox if sb.label == "Menu")
    menu_select.select("View Inventory").run()
    at.run()

    df = at.dataframe[0].value
    assert sku not in df["sku"].values
