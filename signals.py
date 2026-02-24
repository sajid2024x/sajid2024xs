# signals.py
from datetime import timedelta
from weights import WEIGHTS

KEYWORDS = [
    "base",
    "agent",
    "launch",
    "deploy",
    "token",
    "ai"
]

TIME_WINDOW_MINUTES = 20
MIN_WEIGHTED_SCORE = 4


def detect_signals(tweets):
    """
    Takes collected tweets and returns ONE best signal or None.
    """

    if not tweets:
        return None

    tweets_sorted = sorted(tweets, key=lambda x: x["time"])
    best_signal = None

    for keyword in KEYWORDS:
        bucket = []

        for t in tweets_sorted:
            if keyword.lower() in t["text"].lower():
                bucket.append(t)

        for i in range(len(bucket)):
            window = [bucket[i]]
            score = WEIGHTS.get(bucket[i]["type"], 1)

            for j in range(i + 1, len(bucket)):
                if bucket[j]["time"] - bucket[i]["time"] <= timedelta(minutes=TIME_WINDOW_MINUTES):
                    window.append(bucket[j])
                    score += WEIGHTS.get(bucket[j]["type"], 1)

            if score >= MIN_WEIGHTED_SCORE:
                signal = {
                    "keyword": keyword,
                    "score": score,
                    "count": len(window),
                    "accounts": list(set(x["handle"] for x in window)),
                    "start_time": window[0]["time"]
                }

                if not best_signal or signal["score"] > best_signal["score"]:
                    best_signal = signal

    return best_signal
