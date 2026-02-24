# agent.py

import os
import time
import tweepy

from collector import collect_posts
from signals import detect_signals
from predictions import generate_prediction
from storage import store_prediction
from predictions import PREDICTION_HOURS


def main():
    client = tweepy.Client(
        bearer_token=os.getenv("X_BEARER_TOKEN"),
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_SECRET"),
    )

    posts = collect_posts()
    if not posts:
        print("no posts collected.")
        return

    signals = detect_signals(posts)
    if not signals:
        print("no signal detected.")
        return

    # support dict or list signals
    if isinstance(signals, list):
        s = signals[0]
    else:
        s = signals

    prediction_tweet = generate_prediction(s)

    client.create_tweet(text=prediction_tweet)
    print("posted prediction:")
    print(prediction_tweet)
    store_prediction(s, PREDICTION_HOURS)
print("prediction stored for resolution")


if __name__ == "__main__":
    while True:
        main()
        time.sleep(100)
