import cv2
import json
import os
import time

from detector import VehicleDetector
from ml_predictor import MLPredictor
from traffic_controller import SmartTrafficController
from database import TrafficDatabase
from lane_manager import LaneManager
from emergency import EmergencyManager
from config import VIDEO_PATH, WINDOW_NAME


# -----------------------------------
# Initialize Modules
# -----------------------------------

detector = VehicleDetector()
controller = SmartTrafficController()
database = TrafficDatabase()
lane_manager = LaneManager()
emergency = EmergencyManager()
predictor = MLPredictor()


# -----------------------------------
# Create Data Folder
# -----------------------------------

os.makedirs("data", exist_ok=True)


# -----------------------------------
# JSON Update Timer
# -----------------------------------

last_update = 0


# -----------------------------------
# Open Video
# -----------------------------------

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("Error: Cannot open video.")
    exit()


# -----------------------------------
# Main Loop
# -----------------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        print("Video Finished.")
        break


    # -----------------------------------
    # Vehicle Detection
    # -----------------------------------

    total, counts, detections = detector.detect(frame)


    # -----------------------------------
    # Traffic Signal Calculation
    # -----------------------------------

    traffic_level, green_time = controller.calculate_signal(total)

    predicted_green = predictor.predict_green_signal(total)


    # -----------------------------------
    # Lane Calculation
    # -----------------------------------

    lanes = lane_manager.calculate_lanes(
        detections,
        frame
    )

    green_lane = lane_manager.get_green_lane()


    # -----------------------------------
    # Emergency System
    # -----------------------------------

    if lanes[green_lane] >= 10:
        emergency.activate(green_lane)
    else:
        emergency.deactivate()


    status = emergency.get_status()


    if status["active"]:

        green_lane = status["lane"]
        traffic_level = "EMERGENCY"
        green_time = 60


    # -----------------------------------
    # Save Database
    # -----------------------------------

    database.save_data(
        counts["car"],
        counts["bus"],
        counts["truck"],
        counts["motorcycle"],
        total,
        traffic_level,
        green_time
    )


    # -----------------------------------
    # Live Data
    # -----------------------------------

    live_data = {

        "car": counts["car"],
        "bus": counts["bus"],
        "truck": counts["truck"],
        "motorcycle": counts["motorcycle"],

        "total": total,

        "traffic": traffic_level,
        "green": green_time,

        "ai_green_time": predicted_green,

        "North": lanes["North"],
        "South": lanes["South"],
        "East": lanes["East"],
        "West": lanes["West"],

        "green_lane": green_lane,

        "emergency": status["active"],
        "emergency_vehicle": status["vehicle"]
    }


    # -----------------------------------
    # Update JSON Every 1 Second
    # -----------------------------------

    current_time = time.time()

    if current_time - last_update >= 1:

        with open(
            "data/live_data.json",
            "w"
        ) as f:

            json.dump(
                live_data,
                f,
                indent=4
            )

        last_update = current_time
            # -----------------------------------
    # Draw Bounding Boxes
    # -----------------------------------

    for item in detections:

        x1, y1, x2, y2 = item["box"]
        label = item["label"]

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2
        )


    # -----------------------------------
    # Lane Divider
    # -----------------------------------

    height, width = frame.shape[:2]

    cv2.line(
        frame,
        (width//2, 0),
        (width//2, height),
        (255,0,0),
        2
    )

    cv2.line(
        frame,
        (0, height//2),
        (width, height//2),
        (255,0,0),
        2
    )


    # -----------------------------------
    # Vehicle Information
    # -----------------------------------

    cv2.putText(
        frame,
        f"Cars : {counts['car']}",
        (20,30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,255),
        2
    )


    cv2.putText(
        frame,
        f"Buses : {counts['bus']}",
        (20,60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,255),
        2
    )


    cv2.putText(
        frame,
        f"Trucks : {counts['truck']}",
        (20,90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,255),
        2
    )


    cv2.putText(
        frame,
        f"Motorcycles : {counts['motorcycle']}",
        (20,120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,255),
        2
    )


    cv2.putText(
        frame,
        f"Total Vehicles : {total}",
        (20,150),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0,255,255),
        2
    )


    cv2.putText(
        frame,
        f"Traffic : {traffic_level}",
        (20,180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0,255,0),
        2
    )


    cv2.putText(
        frame,
        f"Green Time : {green_time} sec",
        (20,210),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0,0,255),
        2
    )


    cv2.putText(
        frame,
        f"AI Green Time : {predicted_green:.2f} sec",
        (20,240),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,0,255),
        2
    )


    # -----------------------------------
    # Lane Count Display
    # -----------------------------------

    cv2.putText(
        frame,
        f"North : {lanes['North']}",
        (20,280),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,0),
        2
    )


    cv2.putText(
        frame,
        f"South : {lanes['South']}",
        (20,310),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,0),
        2
    )


    cv2.putText(
        frame,
        f"East : {lanes['East']}",
        (20,340),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,0),
        2
    )


    cv2.putText(
        frame,
        f"West : {lanes['West']}",
        (20,370),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,0),
        2
    )


    cv2.putText(
        frame,
        f"Green Lane : {green_lane}",
        (20,400),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,0),
        2
    )
        # -----------------------------------
    # Emergency Display
    # -----------------------------------

    if status["active"]:

        cv2.putText(
            frame,
            "EMERGENCY MODE",
            (20,450),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,0,255),
            3
        )


        cv2.putText(
            frame,
            f"Priority Lane : {green_lane}",
            (20,490),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,255),
            2
        )


    else:

        cv2.putText(
            frame,
            "Normal Mode",
            (20,450),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )


    # -----------------------------------
    # Display Video
    # -----------------------------------

    cv2.imshow(
        WINDOW_NAME,
        frame
    )


    # Press Q to Exit

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break



# -----------------------------------
# Cleanup
# -----------------------------------

cap.release()

cv2.destroyAllWindows()