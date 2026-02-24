# agent.py

import os
import time
import tweepy

from collector import collect_posts
from signals import detect_signals


def main():
    # connect to X
    client = tweepy.Client(
        bearer_token=os.getenv("X_BEARER_TOKEN"),
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_SECRET"),
    )

    # collect posts
    posts = collect_posts()
    if not posts:
        print("no posts collected.")
        return

    # detect signals
    signals = detect_signals(posts)
    if not signals:
        print("no signal detected.")
        return

    # support dict or list signals
    if isinstance(signals, list):
        s = signals[0]
    else:
        s = signals

    # build neutral signal tweet
    tweet = (
        "Signal detected\n\n"
        f"Narrative: {s['keyword']}\n"
        f"Mentions: {s['count']} accounts\n"
        "Window: 20 minutes\n"
        f"Accounts: {', '.join(s['accounts'])}"
    )

    # post to X
    client.create_tweet(text=tweet)
    print("posted signal:")
    print(tweet)


if __name__ == "__main__":
    while True:
        main()
        time.sleep(600)  # run every 10 minutes
