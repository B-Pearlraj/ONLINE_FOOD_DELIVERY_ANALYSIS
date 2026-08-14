import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Online Food Delivery Dashboard",
    page_icon="Logo-PTS.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        /* ---------- General ---------- */
        .main {
            background-color: #f5f6fa;
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        /* ---------- Header ---------- */
        .dashboard-header {
            background: linear-gradient(90deg, #FF4B4B 0%, #FF884B 100%);
            padding: 1.8rem 2rem;
            border-radius: 16px;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 14px rgba(255, 75, 75, 0.25);
        }
        .dashboard-header h1 {
            color: white;
            font-size: 2.1rem;
            font-weight: 800;
            margin: 0;
        }
        .dashboard-header p {
            color: rgba(255,255,255,0.9);
            font-size: 1rem;
            margin-top: 0.3rem;
        }

        /* ---------- KPI Cards ---------- */
        .kpi-card {
            background: white;
            border-radius: 14px;
            padding: 1.1rem 1.3rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
            border-left: 5px solid #FF4B4B;
            height: 100%;
        }
        .kpi-label {
            font-size: 0.82rem;
            font-weight: 600;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            margin-bottom: 0.3rem;
        }
        .kpi-value {
            font-size: 1.6rem;
            font-weight: 800;
            color: #1f2937;
        }
        .kpi-icon {
            font-size: 1.4rem;
            margin-bottom: 0.2rem;
        }

        /* ---------- Section headers ---------- */
        .section-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #1f2937;
            margin: 1.6rem 0 0.8rem 0;
            padding-bottom: 0.4rem;
            border-bottom: 2px solid #FF4B4B33;
        }

        /* ---------- Dataframe container ---------- */
        div[data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        }

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {
            background-color: #1f2937;
        }
        section[data-testid="stSidebar"] * {
            color: #f5f6fa;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------------------------
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


try:
    fddc_df = load_data("Online_Food_Delivery_Cleaned.csv")
except FileNotFoundError:
    st.error("⚠️ Could not find `Online_Food_Delivery_Cleaned.csv`. Please place it in the app directory.")
    st.stop()

# Small helper: does a column exist and is it usable
def has_col(col: str) -> bool:
    return col in fddc_df.columns


# ---------------------------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------------------------
st.sidebar.markdown("## 🔍 Filters")
filtered_df = fddc_df.copy()

if has_col("Order_Status"):
    statuses = sorted(fddc_df["Order_Status"].dropna().unique().tolist())
    selected_statuses = st.sidebar.multiselect(
        "Order Status", options=statuses, default=statuses
    )
    filtered_df = filtered_df[filtered_df["Order_Status"].isin(selected_statuses)]

if has_col("City"):
    cities = sorted(fddc_df["City"].dropna().unique().tolist())
    selected_cities = st.sidebar.multiselect(
        "City", options=cities, default=cities
    )
    filtered_df = filtered_df[filtered_df["City"].isin(selected_cities)]

if has_col("Payment_Method"):
    methods = sorted(fddc_df["Payment_Method"].dropna().unique().tolist())
    selected_methods = st.sidebar.multiselect(
        "Payment Method", options=methods, default=methods
    )
    filtered_df = filtered_df[filtered_df["Payment_Method"].isin(selected_methods)]

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing **{len(filtered_df):,}** of **{len(fddc_df):,}** orders")

if filtered_df.empty:
    st.warning("No data matches the selected filters. Adjust filters in the sidebar.")
    st.stop()
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='text-align:center;'>Created by <b>Pearlraj</b></div>",
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="dashboard-header">
        <h1>🛵 Online Food Delivery Analysis Dashboard</h1>
        <p>End-to-end view of orders, revenue, delivery performance and customer satisfaction</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------------------------
total_orders = len(filtered_df)
total_revenue = filtered_df["Final_Amount"].sum() if has_col("Final_Amount") else 0
avg_order_value = filtered_df["Order_Value"].mean() if has_col("Order_Value") else 0
avg_delivery_time = filtered_df["Delivery_Time_Min"].mean() if has_col("Delivery_Time_Min") else 0

cancellation_rate = (
    (filtered_df["Order_Status"] == "Cancelled").sum() / total_orders * 100
    if has_col("Order_Status") and total_orders
    else 0
)

avg_delivery_rating = filtered_df["Delivery_Rating"].mean() if has_col("Delivery_Rating") else 0
profit_margin = filtered_df["Profit_Margin_Percentage"].mean() if has_col("Profit_Margin_Percentage") else 0


def kpi_card(col, icon, label, value):
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# KPI ROW 1
# ---------------------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
kpi_card(c1, "📦", "Total Orders", f"{total_orders:,}")
kpi_card(c2, "💰", "Total Revenue", f"₹{total_revenue:,.2f}")
kpi_card(c3, "🧾", "Avg Order Value", f"₹{avg_order_value:,.2f}")
kpi_card(c4, "⏱️", "Avg Delivery Time", f"{avg_delivery_time:.1f} min")

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# KPI ROW 2
# ---------------------------------------------------------------------------
c5, c6, c7 = st.columns(3)
kpi_card(c5, "❌", "Cancellation Rate", f"{cancellation_rate:.2f}%")
kpi_card(c6, "⭐", "Avg Delivery Rating", f"{avg_delivery_rating:.2f} / 5")
kpi_card(c7, "📈", "Profit Margin", f"{profit_margin:.2f}%")


# ---------------------------------------------------------------------------
# CHARTS
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">📊 Order & Revenue Insights</div>', unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    if has_col("Order_Status"):
        status_counts = filtered_df["Order_Status"].value_counts().reset_index()
        status_counts.columns = ["Order Status", "Count"]
        fig = px.pie(
            status_counts,
            names="Order Status",
            values="Count",
            hole=0.45,
            title="Order Status Breakdown",
            color_discrete_sequence=px.colors.sequential.Sunsetdark,
        )
        fig.update_traces(textinfo="percent+label")
        fig.update_layout(margin=dict(t=50, b=10, l=10, r=10), height=380)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("`Order_Status` column not found — pie chart skipped.")

with chart_col2:
    if has_col("Delivery_Rating"):
        fig = px.histogram(
            filtered_df,
            x="Delivery_Rating",
            nbins=10,
            title="Delivery Rating Distribution",
            color_discrete_sequence=["#FF4B4B"],
        )
        fig.update_layout(
            margin=dict(t=50, b=10, l=10, r=10),
            height=380,
            bargap=0.15,
            xaxis_title="Rating",
            yaxis_title="Number of Orders",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("`Delivery_Rating` column not found — histogram skipped.")

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    if has_col("Delivery_Time_Min"):
        fig = px.box(
            filtered_df,
            y="Delivery_Time_Min",
            points="outliers",
            title="Delivery Time Spread (min)",
            color_discrete_sequence=["#FF884B"],
        )
        fig.update_layout(margin=dict(t=50, b=10, l=10, r=10), height=380)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("`Delivery_Time_Min` column not found — box plot skipped.")

with chart_col4:
    if has_col("Payment_Method") and has_col("Final_Amount"):
        rev_by_method = (
            filtered_df.groupby("Payment_Method")["Final_Amount"]
            .sum()
            .reset_index()
            .sort_values("Final_Amount", ascending=False)
        )
        fig = px.bar(
            rev_by_method,
            x="Payment_Method",
            y="Final_Amount",
            title="Revenue by Payment Method",
            color="Final_Amount",
            color_continuous_scale="OrRd",
        )
        fig.update_layout(
            margin=dict(t=50, b=10, l=10, r=10),
            height=380,
            xaxis_title="",
            yaxis_title="Revenue (₹)",
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig, use_container_width=True)
    elif has_col("City") and has_col("Final_Amount"):
        rev_by_city = (
            filtered_df.groupby("City")["Final_Amount"]
            .sum()
            .reset_index()
            .sort_values("Final_Amount", ascending=False)
            .head(10)
        )
        fig = px.bar(
            rev_by_city,
            x="City",
            y="Final_Amount",
            title="Top 10 Cities by Revenue",
            color="Final_Amount",
            color_continuous_scale="OrRd",
        )
        fig.update_layout(
            margin=dict(t=50, b=10, l=10, r=10),
            height=380,
            xaxis_title="",
            yaxis_title="Revenue (₹)",
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough columns available for a revenue breakdown chart.")


# ---------------------------------------------------------------------------
# DATASET PREVIEW
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">🧮 Dataset Preview</div>', unsafe_allow_html=True)

preview_rows = st.slider("Rows to preview", min_value=5, max_value=min(100, len(filtered_df)), value=10, step=5)
st.dataframe(filtered_df.head(preview_rows), use_container_width=True)

csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download filtered data as CSV",
    data=csv_bytes,
    file_name="filtered_food_delivery_data.csv",
    mime="text/csv",
)
