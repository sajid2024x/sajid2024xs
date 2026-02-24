# agent.py

import os
import time
import tweepy

from collector import collect_posts
from signals import detect_signals
from predictions import generate_prediction


def main():
    # 1️⃣ connect to X (v2)
    client = tweepy.Client(
        bearer_token=os.getenv("X_BEARER_TOKEN"),
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_SECRET"),
    )

    # 2️⃣ collect recent posts from watched accounts
    posts = collect_posts()

    if not posts:
        print("no posts collected. staying silent.")
        return

    # 3️⃣ detect signals
    signals = detect_signals(posts)

    if not signals:
        print("no signal detected. staying silent.")
        return

    # 4️⃣ generate prediction tweet (V1 = first signal only)
    prediction_tweet = generate_prediction(signals[0])

    # 5️⃣ post prediction to X
    client.create_tweet(text=prediction_tweet)
    print("posted prediction:")
    print(prediction_tweet)


if __name__ == "__main__":
    while True:
        main()
        time.sleep(300)  # run every 5 minutes
