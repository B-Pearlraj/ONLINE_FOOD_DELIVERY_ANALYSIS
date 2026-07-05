import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(
    page_title="Online Food Delivery Dashboard",
    layout="wide"
)

fddc_df = pd.read_csv("Online_Food_Delivery_Cleaned.csv")


total_orders = len(fddc_df)

total_revenue = fddc_df["Final_Amount"].sum()

avg_order_value = fddc_df["Order_Value"].mean()

avg_delivery_time = fddc_df["Delivery_Time_Min"].mean()

cancellation_rate = (
    (fddc_df["Order_Status"] == "Cancelled").sum()
    / total_orders
) * 100

avg_delivery_rating = fddc_df["Delivery_Rating"].mean()

profit_margin = fddc_df["Profit_Margin_Percentage"].mean()


st.title("Online Food Delivery Analysis Dashboard")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

with col2:
    st.metric(
        "Total Revenue",
        f"₹{total_revenue:,.2f}"
    )

with col3:
    st.metric(
        "Average Order Value",
        f"₹{avg_order_value:.2f}"
    )

with col4:
    st.metric(
        "Average Delivery Time",
        f"{avg_delivery_time:.2f} min"
    )

col5, col6, col7 = st.columns(3)

with col5:
    st.metric(
        "Cancellation Rate",
        f"{cancellation_rate:.2f}%"
    )

with col6:
    st.metric(
        "Average Delivery Rating",
        f"{avg_delivery_rating:.2f}"
    )

with col7:
    st.metric(
        "Profit Margin",
        f"{profit_margin:.2f}%"
    )

st.markdown("---")

st.subheader("Dataset Preview")

st.dataframe(fddc_df.head(10))