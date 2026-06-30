# To access files
import os

# Better than pickle in handling large datasets with complex numpy arrays
import joblib

from gesture_filter import GestureFilter

gesture_filter = GestureFilter()
number_filter = GestureFilter()


# Get path to project root
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(CURRENT_DIR)

MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "models",
    "static_model.pkl"
)

NUM_MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "models",
    "num_static_model.pkl"
)

# Load model once when backend starts
try:
    model = joblib.load(MODEL_PATH)
    num_model = joblib.load(NUM_MODEL_PATH)
except FileNotFoundError:
    raise RuntimeError("Models missing.")


# Returns: gesture and confidence
def predict(features, mode):

    # Prediction
    if (mode != "page_jump"):

        # Prediction
        prediction = model.predict([features])[0]

        # Probabilities of it being right (multiple)
        probabilities = model.predict_proba([features])[0]

    else:

        # Prediction
        prediction = num_model.predict([features])[0]

        # Probabilities of it being right (multiple)
        probabilities = num_model.predict_proba([features])[0]


    # Maximum of these probabilities will be the one -> Confidence
    confidence = float(max(probabilities))

    if mode != "page_jump_mode":
        prediction = gesture_filter.update(prediction, confidence)
    else:
        prediction = number_filter.update(prediction, confidence)

    # Returns the values
    return {
        "gesture" : prediction,
        "confidence" : confidence
        }