class LaneManager:

    def __init__(self):
        self.lanes = {
            "North": 0,
            "South": 0,
            "East": 0,
            "West": 0
        }

    def calculate_lanes(self, detections, frame):

        height, width = frame.shape[:2]

        # Reset counts
        self.lanes = {
            "North": 0,
            "South": 0,
            "East": 0,
            "West": 0
        }

        for item in detections:

            x1, y1, x2, y2 = item["box"]

            # Center of the detected vehicle
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            # Assign lane based on position
            if cx < width // 2 and cy < height // 2:
                self.lanes["North"] += 1

            elif cx >= width // 2 and cy < height // 2:
                self.lanes["East"] += 1

            elif cx < width // 2 and cy >= height // 2:
                self.lanes["West"] += 1

            else:
                self.lanes["South"] += 1

        return self.lanes

    def get_green_lane(self):
        return max(self.lanes, key=self.lanes.get)