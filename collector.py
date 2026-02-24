# collector.py
import tweepy
import os
from watcher import WATCHLIST

client = tweepy.Client(
    consumer_key=os.getenv("X_API_KEY"),
    consumer_secret=os.getenv("X_API_SECRET"),
    access_token=os.getenv("X_ACCESS_TOKEN"),
    access_token_secret=os.getenv("X_ACCESS_SECRET"),
    wait_on_rate_limit=True,
)

def collect_latest():
    collected = []

    for item in WATCHLIST:
        handle = item["handle"].replace("@", "")
        try:
            user = client.get_user(username=handle)
            if not user.data:
                continue

            tweets = client.get_users_tweets(
                user.data.id,
                max_results=5,
                tweet_fields=["created_at", "text"]
            )

            if tweets.data:
                for t in tweets.data:
                    collected.append({
                        "handle": handle,
                        "type": item["type"],
                        "text": t.text,
                        "time": t.created_at
                    })

        except Exception as e:
            print("error:", handle, e)

    return collected

if __name__ == "__main__":
    data = collect_latest()
    print("collected", len(data), "tweets")
