# predictions.py

PREDICTION_HOURS = 48


def generate_prediction(signal):
    keyword = signal["keyword"]

    tweet = (
        "🏟️ Prediction Arena\n\n"
        f"Narrative Detected: \"{keyword}\"\n\n"
        "Question:\n"
        f"Will this narrative escalate within {PREDICTION_HOURS}h?\n\n"
        "Reply YES / NO"
    )

    return tweet
