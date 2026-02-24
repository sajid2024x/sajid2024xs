# agent.py

import os
import time
import tweepy

from collector import collect_posts
from signals import detect_signals


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

    s = signals[0]

    tweet = (
        f"Signal detected\n\n"
        f"Narrative: {s['keyword']}\n"
        f"Mentions: {s['count']} accounts\n"
        f"Window: 20 minutes\n"
        f"Accounts: {', '.join(s['accounts'])}"
    )

    client.create_tweet(text=tweet)
    print("posted signal:", tweet)


if __name__ == "__main__":
    while True:
        main()
        time.sleep(600)  # every 10 minutes
