import joblib
import numpy as np

class MLPredictor:

    def __init__(self):
        self.model = joblib.load("traffic_model.pkl")

    def predict_green_signal(self, vehicle_count):

        data = np.array([[vehicle_count]])

        prediction = self.model.predict(data)

        return prediction[0]