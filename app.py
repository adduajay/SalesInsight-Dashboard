
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SalesInsight Dashboard",layout="wide")
st.title("SalesInsight Dashboard")

df=pd.read_csv("sample_sales_data.csv")
df["Date"]=pd.to_datetime(df["Date"])

st.sidebar.header("Filters")
cat=st.sidebar.multiselect("Category",sorted(df.Category.unique()),default=list(df.Category.unique()))
reg=st.sidebar.multiselect("Region",sorted(df.Region.unique()),default=list(df.Region.unique()))
f=df[df.Category.isin(cat)&df.Region.isin(reg)]

c1,c2,c3,c4=st.columns(4)
c1.metric("Revenue",f"${f.Sales.sum():,.0f}")
c2.metric("Orders",len(f))
c3.metric("Avg Order",f"${f.Sales.mean():.2f}")
c4.metric("Top Product",f.groupby("Product")["Sales"].sum().idxmax())

monthly=f.groupby(f["Date"].dt.to_period("M"))["Sales"].sum()
fig,ax=plt.subplots(figsize=(8,3))
monthly.plot(ax=ax)
ax.set_title("Monthly Sales")
st.pyplot(fig)

fig2,ax2=plt.subplots(figsize=(8,4))
f.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(10).plot(kind="bar",ax=ax2)
ax2.set_title("Top Products")
st.pyplot(fig2)

st.download_button("Download Filtered CSV",f.to_csv(index=False),"filtered_sales.csv","text/csv")
