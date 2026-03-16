import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Load the cleaned dataset
data_path = "Cleaned_Bookings_Dataset.xlsx"
df = pd.read_excel(data_path)

# Convert Booking Date to datetime
df["Booking Date"] = pd.to_datetime(df["Booking Date"])
df["Booking Hour"] = df["Booking Date"].dt.hour

# Streamlit App
st.set_page_config(page_title="Booking Dashboard", layout="wide")
st.title("📊 Multi-Service Business Booking Dashboard")

# Sidebar Filters
st.sidebar.header("🔍 Filters")
st.sidebar.write("🔹 Use the sidebar filters to explore the data interactively!")

# Date Range Filter
date_range = st.sidebar.date_input("Select Date Range", [df["Booking Date"].min(), df["Booking Date"].max()], min_value=df["Booking Date"].min(), max_value=df["Booking Date"].max())

# Service Type Filter
service_types = st.sidebar.multiselect("Select Service Type", options=df["Booking Type"].unique(), default=df["Booking Type"].unique())

# Price Range Filter
min_price, max_price = int(df["Price"].min()), int(df["Price"].max())
price_range = st.sidebar.slider("Select Price Range", min_value=min_price, max_value=max_price, value=(min_price, max_price))

# Apply Filters
filtered_df = df[(df["Booking Date"] >= pd.to_datetime(date_range[0])) &
                 (df["Booking Date"] <= pd.to_datetime(date_range[1])) &
                 (df["Booking Type"].isin(service_types)) &
                 (df["Price"] >= price_range[0]) & (df["Price"] <= price_range[1])]

# Show Data Overview
st.subheader("Dataset Overview")
st.dataframe(filtered_df.head())

# Key Metrics
st.subheader("📌 Key Metrics")
total_bookings = len(filtered_df)
total_revenue = filtered_df["Price"].sum()
avg_booking_price = filtered_df["Price"].mean()
st.metric("Total Bookings", total_bookings)
st.metric("Total Revenue ($)", round(total_revenue, 2))
st.metric("Average Booking Price ($)", round(avg_booking_price, 2))

# Booking Trends Over Time
st.subheader("📅 Booking Trends Over Time")
daily_bookings = filtered_df.groupby("Booking Date").size().reset_index(name="Count")
fig = px.line(daily_bookings, x="Booking Date", y="Count", title="Daily Booking Count", markers=True)
st.plotly_chart(fig)

# Service Type Distribution
st.subheader("🔍 Bookings by Service Type")
service_counts = filtered_df["Booking Type"].value_counts().reset_index()
service_counts.columns = ["Service Type", "Count"]
fig2 = px.bar(service_counts, x="Service Type", y="Count", title="Booking Distribution by Service Type", color="Count", text_auto=True)
st.plotly_chart(fig2)

# Monthly Revenue Trend
st.subheader("📈 Monthly Revenue Trend")
filtered_df["Year-Month"] = filtered_df["Booking Date"].dt.to_period("M").astype(str)
monthly_revenue = filtered_df.groupby("Year-Month")["Price"].sum().reset_index()
fig3 = px.line(monthly_revenue, x="Year-Month", y="Price", title="Monthly Revenue", markers=True, labels={"Price": "Revenue ($)"})
st.plotly_chart(fig3)

# Heatmap of Peak Booking Hours
st.subheader("⏰ Peak Booking Hours")
hourly_bookings = filtered_df.groupby("Booking Hour").size().reset_index(name="Count")
fig4 = go.Figure(data=go.Bar(x=hourly_bookings["Booking Hour"], y=hourly_bookings["Count"], marker_color='blue'))
fig4.update_layout(title="Peak Booking Hours", xaxis_title="Hour of the Day", yaxis_title="Number of Bookings")
st.plotly_chart(fig4)

# Customer Spending Analysis
st.subheader("💰 Top Customers by Spending")
top_customers = filtered_df.groupby("Customer Name")["Price"].sum().reset_index().sort_values(by="Price", ascending=False).head(10)
fig5 = px.bar(top_customers, x="Customer Name", y="Price", title="Top 10 Customers by Spending", text_auto=True)
st.plotly_chart(fig5)
