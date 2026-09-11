from ml_predictor import MLPredictor

predictor = MLPredictor()

vehicles = 20

green = predictor.predict_green_signal(vehicles)

print("Vehicles :", vehicles)
print("Predicted Green Signal :", green, "seconds")
