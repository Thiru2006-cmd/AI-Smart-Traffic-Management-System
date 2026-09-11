import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Traffic Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Smart Traffic Analytics")

# -------------------------
# Connect Database
# -------------------------

conn = sqlite3.connect("traffic.db")

df = pd.read_sql_query("SELECT * FROM traffic_data", conn)

conn.close()

# -------------------------
# No Data
# -------------------------

if df.empty:
    st.warning("No traffic data found.")
    st.stop()

# -------------------------
# Statistics
# -------------------------

total_records = len(df)
average_vehicles = round(df["total"].mean(), 2)
highest_traffic = df["total"].max()
lowest_traffic = df["total"].min()

most_common = df["traffic_level"].mode()[0]

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Records", total_records)
c2.metric("Average Vehicles", average_vehicles)
c3.metric("Highest", highest_traffic)
c4.metric("Lowest", lowest_traffic)
c5.metric("Traffic Level", most_common)

st.divider()

# -------------------------
# Vehicle Totals
# -------------------------

vehicle_totals = pd.DataFrame({
    "Vehicle": ["Cars","Buses","Trucks","Motorcycles"],
    "Count":[
        df["cars"].sum(),
        df["buses"].sum(),
        df["trucks"].sum(),
        df["motorcycles"].sum()
    ]
})

left,right = st.columns(2)

with left:

    st.subheader("Vehicle Count")

    fig = px.bar(
        vehicle_totals,
        x="Vehicle",
        y="Count",
        text="Count"
    )

    st.plotly_chart(fig,use_container_width=True)

with right:

    st.subheader("Vehicle Distribution")

    fig = px.pie(
        vehicle_totals,
        values="Count",
        names="Vehicle"
    )

    st.plotly_chart(fig,use_container_width=True)

st.divider()

# -------------------------
# Traffic Trend
# -------------------------

st.subheader("Traffic Trend")

fig = px.line(
    df,
    x="id",
    y="total",
    markers=True,
    title="Vehicle Count Over Time"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# -------------------------
# Traffic Level
# -------------------------

st.subheader("Traffic Level Distribution")

traffic = df["traffic_level"].value_counts().reset_index()
traffic.columns=["Traffic","Count"]

fig = px.bar(
    traffic,
    x="Traffic",
    y="Count",
    color="Traffic"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# -------------------------
# Latest Records
# -------------------------

st.subheader("Latest Traffic Records")

st.dataframe(
    df.sort_values("id",ascending=False),
    use_container_width=True
)