# core/utils.py
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt

def export_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

def export_to_excel(df):
    buffer = BytesIO()
    df.to_excel(buffer, index=False, engine='xlsxwriter')
    return buffer.getvalue()

def plot_inventory_distribution(df):
    fig, ax = plt.subplots()
    ax.bar(df["name"], df["quantity"])
    ax.set_title("Inventory Quantities")
    plt.xticks(rotation=45)
    return fig
