from streamlit.testing.v1 import AppTest
from reset_utils import reset_inventory_db
import time

def test_ai_insights_output():
    reset_inventory_db()

    at = AppTest.from_file("app.py")
    at.run()

    # Step 1: Add a product to ensure inventory isn't empty
    menu_select = next(sb for sb in at.selectbox if sb.label == "Menu")
    menu_select.select("Add Product").run()
    at.run()

    sku = f"TP{int(time.time())}"
    at.text_input[0].input("Insight Test Product")
    at.text_input[1].input(sku)
    at.number_input[0].set_value(1)
    at.number_input[1].set_value(5)
    at.number_input[2].set_value(3.33)
    at.button[0].click().run()

    # Step 2: Open AI Insights section
    menu_select = next(sb for sb in at.selectbox if sb.label == "Menu")
    menu_select.select("AI Insights").run()
    at.run()

    # Step 3: Check if AI summary is populated
    assert len(at.text_area) > 0
    assert "Predicted Stockouts" in at.text_area[0].label
    assert at.text_area[0].value.strip() != ""
