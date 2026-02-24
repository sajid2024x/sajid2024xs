# storage.py

import json
import os
from datetime import datetime, timedelta

FILE = "predictions.json"


def load_predictions():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)


def save_predictions(predictions):
    with open(FILE, "w") as f:
        json.dump(predictions, f, indent=2)


def store_prediction(signal, hours):
    predictions = load_predictions()

    prediction = {
        "keyword": signal["keyword"],
        "accounts": signal["accounts"],
        "posted_at": datetime.utcnow().isoformat(),
        "resolve_at": (datetime.utcnow() + timedelta(hours=hours)).isoformat(),
        "resolved": False
    }

    predictions.append(prediction)
    save_predictions(predictions)
