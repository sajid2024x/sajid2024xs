import os
import random
import tweepy
import time

THOUGHTS = [
    "price moved, but onchain activity stayed flat.",
    "volume increased without a matching rise in active wallets.",
    "short-term wallets are active. long-term holders are not.",
    "transaction count rose, average size did not.",
    "activity looks fragmented, not coordinated."
]

def think():
    return random.choice(THOUGHTS)

def main():
    auth = tweepy.OAuth1UserHandler(
        os.getenv("X_API_KEY"),
        os.getenv("X_API_SECRET"),
        os.getenv("X_ACCESS_TOKEN"),
        os.getenv("X_ACCESS_SECRET"),
    )

    api = tweepy.API(auth)

    tweet = think()
    api.update_status(tweet)
    print("posted:", tweet)

if __name__ == "__main__":
    main()
    time.sleep(60)  # keep container alive
