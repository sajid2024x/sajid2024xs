# predictions.py

PREDICTION_HOURS = 48


def generate_prediction(signal):
    """
    Takes ONE signal dict and returns prediction tweet text
    """

    keyword = signal["keyword"]

    tweet = f"""🏟️ Prediction Arena

Narrative Detected: "{keyword}"

Question:
Will this narrative escalate within {PREDICTION_HOURS}h?

Reply YES / NO
"""
    return tweet
