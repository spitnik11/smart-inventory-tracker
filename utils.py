import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def export_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

def export_to_excel(df):
    buffer = BytesIO()
    df.to_excel(buffer, index=False, engine='xlsxwriter')
    return buffer.getvalue()

def plot_inventory_distribution(df):
    fig, ax = plt.subplots()
    ax.bar(df["name"], df["quantity"])
    plt.xticks(rotation=45)
    return fig