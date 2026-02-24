# signals.py
from datetime import timedelta

KEYWORDS = [
    "base",
    "agent",
    "launch",
    "deploy",
    "token",
    "ai"
]

TIME_WINDOW_MINUTES = 20
MIN_MENTIONS = 3


def detect_signals(tweets):
    tweets_sorted = sorted(tweets, key=lambda x: x["time"])
    best_signal = None

    for keyword in KEYWORDS:
        bucket = []

        for t in tweets_sorted:
            if keyword.lower() in t["text"].lower():
                bucket.append(t)

        for i in range(len(bucket)):
            window = [bucket[i]]

            for j in range(i + 1, len(bucket)):
                if bucket[j]["time"] - bucket[i]["time"] <= timedelta(minutes=TIME_WINDOW_MINUTES):
                    window.append(bucket[j])

            if len(window) >= MIN_MENTIONS:
                signal = {
                    "keyword": keyword,
                    "count": len(window),
                    "accounts": list(set(x["handle"] for x in window)),
                    "start_time": window[0]["time"]
                }

                # keep the strongest signal only
                if not best_signal or signal["count"] > best_signal["count"]:
                    best_signal = signal

    return best_signal
