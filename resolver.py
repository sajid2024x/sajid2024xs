# resolver.py

import json
from datetime import datetime, timedelta
from signals import detect_signals
from collector import collect_posts


RESOLUTION_THRESHOLD_MENTIONS = 3
RESOLUTION_THRESHOLD_ACCOUNTS = 3


def load_predictions():
    try:
        with open("predictions.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_predictions(predictions):
    with open("predictions.json", "w") as f:
        json.dump(predictions, f, default=str, indent=2)


def resolve_predictions():
    predictions = load_predictions()
    now = datetime.utcnow()

    updated = False
    resolution_messages = []

    for p in predictions:
        if p.get("resolved"):
            continue

        resolve_time = datetime.fromisoformat(p["resolve_at"])
        if now < resolve_time:
            continue

        posts = collect_posts()
        signals = detect_signals(posts)

        outcome = "NO"
        for s in signals:
            if s["keyword"] == p["keyword"]:
                if (
                    s["count"] >= RESOLUTION_THRESHOLD_MENTIONS
                    and len(s["accounts"]) >= RESOLUTION_THRESHOLD_ACCOUNTS
                ):
                    outcome = "YES"

        p["resolved"] = True
        p["outcome"] = outcome
        p["resolved_at"] = now.isoformat()
        updated = True

        resolution_messages.append({
            "keyword": p["keyword"],
            "outcome": outcome,
            "accounts": p["accounts"]
        })

    if updated:
        save_predictions(predictions)

    return resolution_messages
