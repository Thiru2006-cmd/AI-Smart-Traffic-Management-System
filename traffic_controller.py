class SmartTrafficController:

    def calculate_signal(self, vehicle_count):

        if vehicle_count <= 10:
            return "LOW", 15

        elif vehicle_count <= 20:
            return "MEDIUM", 30

        elif vehicle_count <= 40:
            return "HIGH", 45

        else:
            return "VERY HIGH", 60