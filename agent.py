import os
import tweepy
import random

THOUGHTS = [
    "price moved, but onchain activity stayed flat.",
    "volume increased without a matching rise in active wallets.",
    "short-term wallets are active. long-term holders are not.",
    "transaction count rose, average size did not.",
    "activity looks fragmented, not coordinated.",
    "recent moves are dominated by small transfers."
]

def think():
    return random.choice(THOUGHTS)

auth = tweepy.OAuth1UserHandler(
    os.getenv("X_API_KEY"),
    os.getenv("X_API_SECRET"),
    os.getenv("X_ACCESS_TOKEN"),
    os.getenv("X_ACCESS_SECRET")
)

x_api = tweepy.API(auth)

if __name__ == "__main__":
    tweet = think()
    x_api.update_status(tweet)
    print("posted:", tweet)
