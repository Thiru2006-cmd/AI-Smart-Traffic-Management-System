import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Connect to database
conn = sqlite3.connect("traffic.db")

# Read data from database
query = """
SELECT
    total,
    green_signal
FROM traffic_data
"""

df = pd.read_sql_query(query, conn)

conn.close()

print(df.head())

# Check whether enough data is available
if len(df) < 10:
    print("Not enough data to train the model.")
    exit()

# Features
X = df[["total"]]

# Target
y = df["green_signal"]

# Train model
model = LinearRegression()

model.fit(X, y)

# Save model
joblib.dump(model, "traffic_model.pkl")

print("\nModel trained successfully!")
print("traffic_model.pkl created successfully!")

# Test prediction
future_vehicle_count = [[25]]

prediction = model.predict(future_vehicle_count)

print("-----------------------------------")
print("Predicted Vehicles :", future_vehicle_count[0][0])
print("Recommended Green Signal :", round(prediction[0], 2), "seconds")
print("-----------------------------------")