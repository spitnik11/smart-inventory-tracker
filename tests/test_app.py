from streamlit.testing.v1 import AppTest
from reset_utils import reset_inventory_db
import time

def test_update_quantity():
    reset_inventory_db()

    at = AppTest.from_file("app.py")
    at.run()

    # Step 1: Add product
    at.selectbox[0].select("Add Product").run()
    at.run()

    sku = f"TP{int(time.time())}"
    at.text_input[0].input("Test Product")
    at.text_input[1].input(sku)
    at.number_input[0].set_value(10)
    at.number_input[1].set_value(3)
    at.number_input[2].set_value(4.99)
    at.button[0].click().run()

    # Step 2: Update Quantity
    at.selectbox[0].select("Update Quantity").run()
    at.run()

    # Select SKU dropdown by label
    sku_selectbox = next(sb for sb in at.selectbox if sb.label == "Select SKU")
    sku_selectbox.select(sku).run()

    at.number_input[0].set_value(5)
    at.button[0].click().run()

    #  Re-initialize AppTest to reset widget tree
    at = AppTest.from_file("app.py")
    at.run()

    #  Now safely go to "View Inventory"
    at.selectbox[0].select("View Inventory").run()
    at.run()

    df = at.dataframe[0].value
    updated_row = df[df["sku"] == sku]
    assert not updated_row.empty
    assert updated_row["quantity"].iloc[0] == 15
