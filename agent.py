# agent.py

import os
import time
import tweepy

from collector import collect_latest
from signals import detect_signals
from interpretations import interpret_signal
from reporter import generate_report


def run_cycle():
    # 1️⃣ connect to X (v2)
    client = tweepy.Client(
        bearer_token=os.getenv("X_BEARER_TOKEN"),
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_SECRET"),
        wait_on_rate_limit=True,
    )

    # 2️⃣ collect recent posts
    posts = collect_latest()

    if not posts:
        print("no posts collected. staying silent.")
        return

    # 3️⃣ detect signals
    signals = detect_signals(posts)

    if not signals:
        print("no signal detected. staying silent.")
        return

    # 4️⃣ pick the strongest signal
    strongest = max(signals, key=lambda s: s["count"])

    # 5️⃣ interpret signal
    interpretation = interpret_signal(strongest)

    if not interpretation:
        print("signal not strong enough to report.")
        return

    # 6️⃣ generate report
    tweet = generate_report(interpretation)

    if not tweet:
        print("report empty. aborting post.")
        return

    # 7️⃣ post
    client.create_tweet(text=tweet)
    print("posted intelligence report:")
    print(tweet)


if __name__ == "__main__":
    while True:
        run_cycle()
        time.sleep(300)  # every 5 minutes
