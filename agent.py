import os
import random
import tweepy

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
    client = tweepy.Client(
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_SECRET"),
    )

    tweet = think()
    client.create_tweet(text=tweet)
    print("posted:", tweet)

if __name__ == "__main__":
    main()
