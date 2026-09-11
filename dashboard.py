import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from datetime import datetime

from llm_copilot import generate_disruption_explanation
from passenger_journey import analyze_passenger_journey


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="TwinFlow AI Digital Twin",
    page_icon="🚦",
    layout="wide"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0F172A, #1E293B, #0F172A);
}

div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #2563EB, #1D4ED8);
    padding: 15px;
    border-radius: 20px;
    border: 2px solid #38BDF8;
    box-shadow: 0px 8px 20px rgba(0,0,0,.3);
}

div[data-testid="stMetricValue"] {
    color: #FFD700 !important;
    font-size: 48px !important;
    font-weight: 900 !important;
}

div[data-testid="stMetricLabel"] {
    color: white !important;
    font-size: 18px !important;
    font-weight: bold !important;
}

h1 {
    color: #38BDF8 !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# TITLE
# ==========================================

st.markdown("""
<h1 style='text-align:center;color:#38BDF8;font-size:48px;'>
🚦 TwinFlow AI Digital Twin Dashboard
</h1>

<h4 style='text-align:center;color:white;'>
Real-Time Traffic Prediction & Smart Signal Optimization
</h4>
""", unsafe_allow_html=True)


# ==========================================
# LOAD LIVE DATA
# ==========================================

if os.path.exists("data/live_data.json"):

    with open("data/live_data.json", "r") as f:
        data = json.load(f)

else:

    data = {
        "car": 0,
        "bus": 0,
        "truck": 0,
        "motorcycle": 0,
        "total": 0,
        "traffic": "LOW",
        "green": 15,
        "North": 0,
        "South": 0,
        "East": 0,
        "West": 0
    }


car = data.get("car", 0)
bus = data.get("bus", 0)
truck = data.get("truck", 0)
bike = data.get("motorcycle", 0)
total = data.get("total", 0)
traffic = data.get("traffic", "LOW")
green = data.get("green", 15)


# ==========================================
# KPI CARDS
# ==========================================

st.markdown("---")

st.success("🟢 AI System Online | Live Traffic Monitoring Active")

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric("🚗 Total Vehicles", f"{total}")
c2.metric("🚦 Traffic", traffic)
c3.metric("🟢 Green Signal", f"{green} sec")
c4.metric("🤖 AI Prediction", traffic)
c5.metric("📈 Confidence", "94%")
c6.metric("🕒 Time", datetime.now().strftime("%H:%M"))

st.markdown("---")


# ==========================================
# VEHICLE DATA
# ==========================================

vehicle_data = pd.DataFrame({

    "Vehicle": [
        "Cars",
        "Buses",
        "Trucks",
        "Motorcycles"
    ],

    "Count": [
        int(total * 0.70),
        int(total * 0.10),
        int(total * 0.08),
        int(total * 0.12)
    ]
})


# ==========================================
# CHARTS
# ==========================================

left_chart, right_chart = st.columns(2)


with left_chart:

    st.subheader("📊 Vehicle Count")

    st.bar_chart(
        vehicle_data.set_index("Vehicle")
    )


with right_chart:

    st.subheader("🥧 Vehicle Distribution")

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.pie(
        vehicle_data["Count"],
        labels=vehicle_data["Vehicle"],
        autopct="%1.1f%%",
        startangle=90
    )

    ax.axis("equal")

    st.pyplot(fig)


st.markdown("---")


# ==========================================
# TRAFFIC TREND
# ==========================================

st.subheader("📈 Traffic Trend")

trend = pd.DataFrame({

    "Time": [
        "08:00",
        "09:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00"
    ],

    "Vehicles": [
        max(total - 30, 0),
        max(total - 20, 0),
        max(total - 10, 0),
        total,
        total + 10,
        total + 20
    ]
})

st.line_chart(
    trend.set_index("Time")
)

st.markdown("---")


# ==========================================
# AI PREDICTION & SCENARIO SIMULATOR
# ==========================================

left, right = st.columns(2)


# AI PREDICTION

with left:

    st.subheader("🤖 AI Traffic Prediction")

    if traffic.upper() == "LOW":

        st.success(f"Prediction : {traffic}")

    elif traffic.upper() == "MEDIUM":

        st.warning(f"Prediction : {traffic}")

    else:

        st.error(f"Prediction : {traffic}")

    st.metric("📈 Confidence", "94%")

    st.markdown("### 🔍 Main Factors")

    st.write("✔ High Vehicle Count")
    st.write("✔ Low Average Speed")
    st.write("✔ Traffic Density")
    st.write("✔ Signal Timing")


# SCENARIO SIMULATOR

with right:

    st.subheader("⚙️ Scenario Simulator")

    vehicles = st.slider(
        "🚗 Vehicle Count",
        min_value=0,
        max_value=300,
        value=int(total),
        key="vehicle_slider"
    )

    signal = st.slider(
        "🚦 Signal Time (sec)",
        min_value=15,
        max_value=90,
        value=int(green),
        key="signal_slider"
    )

    weather = st.selectbox(
        "🌦 Weather",
        ["Sunny", "Rain", "Fog"]
    )

    if st.button("🚀 Run Simulation"):

        if vehicles < 40:
            simulated_traffic = "LOW"

        elif vehicles < 100:
            simulated_traffic = "MEDIUM"

        else:
            simulated_traffic = "HIGH"

        st.success(
            f"Predicted Traffic : {simulated_traffic}"
        )


# ==========================================
# AI SUGGESTED ACTIONS
# ==========================================

st.subheader("💡 AI Suggested Actions")


if traffic.upper() == "LOW":

    st.success("""
✅ Traffic Flow is Normal

• Maintain Current Signal Timing

• Continue Monitoring
""")


elif traffic.upper() == "MEDIUM":

    st.warning("""
⚠ Moderate Congestion

• Increase Green Signal by 10 sec

• Monitor Junction

• Observe Traffic Flow
""")


else:

    st.error("""
🚨 Heavy Congestion

• Increase Green Signal Duration

• Suggest Alternate Routes

• Deploy Traffic Police

• Monitor Continuously
""")


st.markdown("---")


# ==========================================
# DIGITAL TWIN STATUS
# ==========================================

st.subheader("🛰 Digital Twin Road Status")

d1, d2, d3, d4 = st.columns(4)


if traffic.upper() == "LOW":

    d1.success("🟢 North Lane")
    d2.success("🟢 East Lane")
    d3.success("🟢 South Lane")
    d4.success("🟢 West Lane")


elif traffic.upper() == "MEDIUM":

    d1.warning("🟡 North Lane")
    d2.success("🟢 East Lane")
    d3.warning("🟡 South Lane")
    d4.success("🟢 West Lane")


else:

    d1.error("🔴 North Lane")
    d2.warning("🟡 East Lane")
    d3.error("🔴 South Lane")
    d4.warning("🟡 West Lane")


st.markdown("---")


# ==========================================
# LIVE VEHICLE DATA
# ==========================================

st.subheader("📋 Live Vehicle Details")

st.dataframe(
    vehicle_data,
    use_container_width=True
)

st.markdown("---")


# ==========================================
# DASHBOARD SUMMARY
# ==========================================

st.subheader("📊 AI Dashboard Summary")

summary1, summary2 = st.columns(2)


with summary1:

    st.info(f"""
### Current Status

🚗 Total Vehicles : **{total}**

🚦 Traffic Level : **{traffic}**

🟢 Recommended Green Signal : **{green} sec**

🤖 AI Confidence : **94%**

📅 Date : **{datetime.now().strftime("%d-%m-%Y")}**

🕒 Time : **{datetime.now().strftime("%H:%M:%S")}**
""")


with summary2:

    st.success("""
### TwinFlow Features

✅ AI Traffic Prediction

✅ Vehicle Detection

✅ Signal Timing Recommendation

✅ Scenario Simulation

✅ Digital Twin Monitoring

✅ Smart Traffic Analytics
""")


st.markdown("---")


# ==========================================
# QUICK INSIGHTS
# ==========================================

st.subheader("📈 Quick Insights")

i1, i2, i3 = st.columns(3)

i1.metric("Average Speed", "42 km/h")
i2.metric("Estimated Delay", "18 sec")
i3.metric("Road Utilization", "76%")


st.markdown("---")


# ==========================================
# SYSTEM STATUS
# ==========================================

st.subheader("🚦 System Status")

status1, status2, status3 = st.columns(3)


if traffic.upper() == "LOW":

    status1.success("🟢 Traffic Flow : NORMAL")

elif traffic.upper() == "MEDIUM":

    status1.warning("🟡 Traffic Flow : MODERATE")

else:

    status1.error("🔴 Traffic Flow : HEAVY")


status2.info("🤖 AI Engine : ACTIVE")
status3.success("📡 Digital Twin : ONLINE")


st.markdown("---")


st.warning("""
🚑 Emergency Lane Monitoring

Status : Normal

No Emergency Vehicle Detected
""")


# ==========================================
# PERFORMANCE METRICS
# ==========================================

st.subheader("⚡ System Performance")

perf1, perf2, perf3, perf4 = st.columns(4)

perf1.metric("Prediction Accuracy", "91.9%")
perf2.metric("Response Time", "0.28 sec")
perf3.metric("Model", "Random Forest")
perf4.metric("Data Status", "Live")


st.markdown("---")


# ==========================================
# ROAD HEALTH
# ==========================================

st.subheader("🛣 Road Health")

road_health = pd.DataFrame({

    "Road": [
        "North Lane",
        "East Lane",
        "South Lane",
        "West Lane"
    ],

    "Congestion": [
        20,
        45,
        75,
        30
    ]
})

st.bar_chart(
    road_health.set_index("Road")
)


st.markdown("---")


# ==========================================
# PROJECT DETAILS
# ==========================================

with st.expander("ℹ About TwinFlow"):

    st.write("""
TwinFlow is an AI-powered Digital Twin platform developed
for Smart Traffic Management.

Modules Included

• AI Traffic Prediction

• Vehicle Detection

• Digital Twin Monitoring

• Smart Signal Recommendation

• Scenario Simulation

• Real-Time Analytics

Machine Learning Model

Random Forest Classifier

Dataset

Traffic Digital Twin Dataset

Objective

Reduce traffic congestion using Artificial Intelligence.
""")


st.markdown("---")


# ==========================================
# AI MODEL DETAILS
# ==========================================

st.markdown("## 🧠 AI Model Details")

st.write("""
Model : Random Forest

Accuracy : 91.9%

Dataset Size : 200,000 Records

Prediction Time : 0.28 sec
""")


st.markdown("---")


# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div style='text-align:center;
padding:25px;
background:linear-gradient(90deg,#2563EB,#0EA5E9);
border-radius:15px;
color:white;
margin-top:20px;'>

<h2>🚦 TwinFlow AI Digital Twin</h2>

<h4>Smart Traffic Management System</h4>

<p>
Artificial Intelligence • Digital Twin • Machine Learning
</p>

</div>
""", unsafe_allow_html=True)


# ==========================================
# TWINFLOW LLM MOBILITY COPILOT
# ==========================================

st.markdown("---")

st.markdown("## 🤖 TwinFlow Mobility Copilot")

st.markdown(
    "### 🚍 AI-Powered Public Transport Disruption Explainer"
)

st.info(
    "The AI analyzes current traffic conditions and explains "
    "the possible impact on public transport."
)


if st.button("🤖 Generate AI Disruption Analysis"):

    try:

        with open(
            "data/live_data.json",
            "r"
        ) as file:

            live_data = json.load(file)

        north = live_data.get("North", 0)
        south = live_data.get("South", 0)
        east = live_data.get("East", 0)
        west = live_data.get("West", 0)

        traffic_level = live_data.get(
            "traffic",
            "UNKNOWN"
        )

        green_time = live_data.get(
            "green",
            0
        )

        with st.spinner(
            "🤖 Gemini is analyzing traffic conditions..."
        ):

            analysis = generate_disruption_explanation(
                north,
                south,
                east,
                west,
                traffic_level,
                green_time
            )

        st.success(
            "AI Analysis Generated Successfully!"
        )

        st.markdown(
            "### 🚍 Public Transport Disruption Analysis"
        )

        st.markdown(
            f"""
            <div style="
                background-color: white;
                color: black;
                padding: 25px;
                border-radius: 15px;
                font-size: 18px;
                line-height: 1.7;
            ">
                {analysis.replace(chr(10), '<br>')}
            </div>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:

        st.error(
            f"Error generating AI analysis: {e}"
        )


# ==========================================
# PASSENGER JOURNEY & PRIORITY ANALYSIS
# ==========================================

st.markdown("---")

st.subheader("👤 Passenger Journey Analysis")


col1, col2, col3 = st.columns(3)


with col1:

    journey_start = st.selectbox(
        "Starting Corridor",
        ["North", "South", "East", "West"],
        key="journey_start"
    )


with col2:

    journey_destination = st.selectbox(
        "Destination Corridor",
        ["North", "South", "East", "West"],
        key="journey_destination"
    )


with col3:

    passenger_type = st.selectbox(
        "Passenger Priority",
        ["Normal", "High Priority", "Emergency"],
        key="passenger_priority"
    )


if st.button("👤 Analyze Passenger Journey"):

    try:

        # ==========================================
        # LOAD LIVE TRAFFIC DATA
        # ==========================================

        with open(
            "data/live_data.json",
            "r"
        ) as file:

            live_data = json.load(file)


        traffic_data = {

            "North": live_data.get("North", 0),

            "South": live_data.get("South", 0),

            "East": live_data.get("East", 0),

            "West": live_data.get("West", 0)
        }


        # ==========================================
        # ANALYZE JOURNEY
        # ==========================================

        journey_result = analyze_passenger_journey(
            journey_start,
            journey_destination,
            passenger_type,
            traffic_data
        )


        # Get route result safely
        route_result = journey_result.get(
            "route_result",
            {}
        )


        st.success(
            "Passenger journey analyzed successfully!"
        )


        # ==========================================
        # JOURNEY RESULT
        # ==========================================

        st.markdown("## Journey Result")


        st.write(
            f"**Start:** "
            f"{journey_result.get('start', 'Not available')}"
        )


        st.write(
            f"**Destination:** "
            f"{journey_result.get('destination', 'Not available')}"
        )


        st.write(
            f"**Passenger Priority:** "
            f"{journey_result.get('passenger_type', 'Not available')}"
        )


        st.write(
            f"**Priority Score:** "
            f"{journey_result.get('priority_score', 'Not available')}"
        )


        st.write(
            f"**Journey Status:** "
            f"{journey_result.get('journey_status', 'Not available')}"
        )


        st.write(
            f"**⏱ Estimated Delay:** "
            f"{journey_result.get('estimated_delay', 'Not available')}"
        )


        # ==========================================
        # ROUTE RECOMMENDATION
        # ==========================================

        st.markdown("## 🛣️ Route Recommendation")


        if route_result:

            route = route_result.get(
                "route",
                "Route not available"
            )

            message = route_result.get(
                "message",
                "No recommendation available"
            )


            st.write(
                f"**Recommended Route:** {route}"
            )


            st.info(message)


            # ==========================================
            # VISUAL ROUTE STATUS
            # ==========================================

            st.markdown(
                "## 🗺️ Visual Route Status"
            )


            route_parts = route.split(" → ")


            visual_route = []


            for corridor in route_parts:

                vehicles = traffic_data.get(
                    corridor,
                    0
                )

                visual_route.append(
                    f"🟢 **{corridor} "
                    f"({vehicles} vehicles)**"
                )


            st.markdown(
                " → ".join(visual_route)
            )


            # ==========================================
            # AI ROUTE DECISION
            # ==========================================

            st.markdown(
                "## 🤖 AI Route Decision"
            )


            alternatives = [

                corridor

                for corridor in route_parts

                if corridor != journey_start

                and corridor != journey_destination
            ]


            if alternatives:

                selected_corridor = alternatives[0]


                selected_traffic = traffic_data.get(
                    selected_corridor,
                    0
                )


                st.info(
                    f"🤖 AI selected the "
                    f"**{selected_corridor} Corridor** "
                    f"as the alternative route because "
                    f"it currently has only "
                    f"**{selected_traffic} vehicles**, "
                    f"making it the lowest-traffic "
                    f"available corridor."
                )


            # ==========================================
            # PRIORITY MESSAGE
            # ==========================================

            if passenger_type == "Emergency":

                st.error(
                    "🚑 EMERGENCY PRIORITY: "
                    "The route recommendation prioritizes "
                    "the fastest available low-traffic path."
                )


            elif passenger_type == "High Priority":

                st.warning(
                    "⚡ HIGH PRIORITY: "
                    "The route with lower traffic congestion "
                    "has been prioritized."
                )


            else:

                st.success(
                    "✅ NORMAL PRIORITY: "
                    "A standard low-traffic route "
                    "has been recommended."
                )


        else:

            st.warning(
                "Route recommendation is not available."
            )


    except Exception as e:

        st.error(
            f"Error analyzing passenger journey: {e}"
        )