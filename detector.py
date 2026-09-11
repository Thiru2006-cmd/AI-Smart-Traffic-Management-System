from ultralytics import YOLO

class VehicleDetector:

    def __init__(self):
        self.model = YOLO("models/yolov8n.pt")

        self.vehicle_classes = [
            "car",
            "bus",
            "truck",
            "motorcycle"
        ]

    def detect(self, frame):

        results = self.model(frame, verbose=False)

        counts = {
            "car": 0,
            "bus": 0,
            "truck": 0,
            "motorcycle": 0
        }

        detections = []

        for result in results:
            for box in result.boxes:

                cls = int(box.cls[0])
                label = self.model.names[cls]

                if label in self.vehicle_classes:

                    counts[label] += 1

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    detections.append({
                        "label": label,
                        "box": (x1, y1, x2, y2)
                    })

        total = sum(counts.values())

        return total, counts, detections