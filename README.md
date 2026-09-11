# 🚦 AI Smart Traffic Management System

An AI-powered Smart Traffic Management System designed to optimize traffic signals, analyze vehicle density, predict traffic conditions, and provide priority to emergency vehicles.

## 📌 Project Overview

Traffic congestion is a major problem in modern cities. Traditional traffic signals use fixed timing and cannot dynamically respond to changing traffic conditions.

Our system uses Artificial Intelligence, Machine Learning, Computer Vision, and real-time traffic analytics to intelligently manage traffic at an intersection.

## 🎯 Objectives

- Detect and count vehicles automatically.
- Analyze traffic density in different lanes.
- Dynamically calculate traffic signal timing.
- Predict future traffic conditions using Machine Learning.
- Give priority to emergency vehicles.
- Recommend low-traffic routes.
- Provide real-time traffic analytics through a dashboard.
- Generate intelligent traffic/disruption explanations.

## ✨ Key Features

### 🚗 Vehicle Detection
YOLOv8 is used to detect:

- Cars
- Buses
- Trucks
- Motorcycles

### 🚦 Smart Traffic Signal
Signal duration is dynamically calculated based on the detected traffic volume.

### 🛣️ Lane-wise Traffic Analysis
Traffic is analyzed across:

- North
- South
- East
- West

The system can identify the lane/corridor with higher traffic and recommend signal priority.

### 🤖 Machine Learning Traffic Prediction
A Machine Learning model predicts the recommended green-signal duration based on vehicle count.

### 🚑 Emergency Vehicle Priority
Emergency mode can prioritize an emergency route and provide priority to the selected corridor.

### 🗺️ Route Recommendation
The system analyzes traffic conditions and recommends a lower-traffic route.

### 📊 Real-Time Dashboard
A Streamlit dashboard displays traffic information, lane status, route recommendations, and AI-generated insights.

### 🧠 RAG + LLM
The system includes an AI-powered public transport disruption explainer.

RAG retrieves relevant contextual information, while the LLM uses the retrieved context together with traffic information to generate an understandable analysis.

## 🏗️ System Architecture

```text
                 Camera / Video
                       ↓
                  YOLOv8 Model
                       ↓
               Vehicle Detection
                       ↓
              Vehicle Classification
                       ↓
              Lane-wise Traffic Data
                       ↓
          ┌────────────┴────────────┐
          ↓                         ↓
   Smart Signal Control       ML Prediction
          ↓                         ↓
          └────────────┬────────────┘
                       ↓
              Traffic Database
                       ↓
              Streamlit Dashboard
                       ↓
              AI Decision Support
                  ↓          ↓
                 RAG        LLM
                  ↓          ↓
              Disruption Explanation
