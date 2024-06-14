import pandas as pd
import streamlit as st
from io import BytesIO

def download_excel(df, button_label):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Report', index=False)
    excel_data = buffer.getvalue()
    return excel_data, f"{button_label}.xlsx"