import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SalesInsight Dashboard", layout="wide")
st.title("📊 SalesInsight Dashboard")
uploaded_file = st.sidebar.file_uploader(
    "Upload Sales CSV",
    type=["csv"]
)
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("CSV uploaded successfully!")
else:
    st.info("Please upload a CSV file to continue.")
    st.stop()

if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"])

st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

region = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

filtered_df = df[
    (df["Category"].isin(category)) &
    (df["Region"].isin(region))
]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${filtered_df['Sales'].sum():,.2f}")
col2.metric("Total Orders", len(filtered_df))
col3.metric("Average Order Value", f"${filtered_df['Sales'].mean():,.2f}")
col4.metric(
    "Top Product",
    filtered_df.groupby("Product")["Sales"].sum().idxmax()
)

st.subheader("Monthly Sales Trend")

monthly_sales = filtered_df.groupby(
    filtered_df["Date"].dt.to_period("M")
)["Sales"].sum()

fig, ax = plt.subplots(figsize=(10, 4))
monthly_sales.plot(ax=ax)
ax.set_xlabel("Month")
ax.set_ylabel("Sales")
st.pyplot(fig)


st.subheader("Top Selling Products")

fig2, ax2 = plt.subplots(figsize=(10, 4))
filtered_df.groupby("Product")["Sales"].sum() \
    .sort_values(ascending=False) \
    .head(10) \
    .plot(kind="bar", ax=ax2)

st.pyplot(fig2)


st.download_button(
    "Download Filtered Data",
    filtered_df.to_csv(index=False),
    "filtered_sales.csv",
    "text/csv"
)
