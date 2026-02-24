# agent.py

import os
import tweepy

from collector import collect_latest
from signals import detect_signals
from reporter import generate_report
from interpretations import INTERPRETATIONS


# -------------------------
# X CLIENT
# -------------------------

def get_client():
    return tweepy.Client(
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_SECRET"),
        wait_on_rate_limit=True,
    )


# -------------------------
# SIGNAL SCORING
# -------------------------

def score_signal(signal):
    """
    Very simple, explainable scoring.
    """
    score = 0

    score += signal["count"]          # number of accounts
    score += 2 if signal["count"] >= 3 else 0

    if score >= 7:
        return "strong"
    elif score >= 4:
        return "medium"
    else:
        return "weak"


# -------------------------
# POST INTEL REPORT
# -------------------------

def post_report(client, signal):
    strength = score_signal(signal)

    # choose interpretation based on strength
    interpretation = INTERPRETATIONS[strength][0]

    base_report = generate_report(signal)
    final_text = f"{base_report}\n\n{interpretation}"

    # X safety limit
    if len(final_text) > 270:
        final_text = final_text[:267] + "..."

    client.create_tweet(text=final_text)
    print(f"🛰️ posted {strength} signal for '{signal['keyword']}'")


# -------------------------
# MAIN LOOP
# -------------------------

def main():
    client = get_client()

    # 1. collect tweets
    tweets = collect_latest()
    if not tweets:
        print("no new tweets")
        return

    # 2. detect signals
    signals = detect_signals(tweets)
    if not signals:
        print("no signals detected")
        return

    # 3. post only meaningful signals
    for signal in signals:
        strength = score_signal(signal)

        # posting rules (IMPORTANT)
        if strength in ["medium", "strong"]:
            post_report(client, signal)


if __name__ == "__main__":
    main()
