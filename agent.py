# agent.py

import os
import tweepy

from collector import collect_posts
from signals import detect_signals
from interpretations import interpret_signal
from reporter import generate_report


def main():
    # 1️⃣ connect to X (v2)
    client = tweepy.Client(
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
    signal = detect_signals(posts)

    if not signal:
        print("no signal detected. staying silent.")
        return

    # 4️⃣ interpret the signal
    interpretation = interpret_signal(signal)

    if not interpretation:
        print("signal detected but not strong enough to report.")
        return

    # 5️⃣ generate final report text
    tweet = generate_report(interpretation)

    if not tweet:
        print("report empty. aborting post.")
        return

    # 6️⃣ post to X
    client.create_tweet(text=tweet)
    print("posted intelligence report:")
    print(tweet)


if __name__ == "__main__":
    main()
