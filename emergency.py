class EmergencyManager:

    def __init__(self):
        self.emergency = False
        self.vehicle = ""
        self.priority_lane = ""

    def activate(self, lane, vehicle="Ambulance"):
        self.emergency = True
        self.vehicle = vehicle
        self.priority_lane = lane

    def deactivate(self):
        self.emergency = False
        self.vehicle = ""
        self.priority_lane = ""

    def get_status(self):
        return {
            "active": self.emergency,
            "vehicle": self.vehicle,
            "lane": self.priority_lane
        }