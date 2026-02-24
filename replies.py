# replies.py
import tweepy
import os

def collect_replies(prediction_tweet_id):
    client = tweepy.Client(
        bearer_token=os.getenv("X_BEARER_TOKEN"),
        wait_on_rate_limit=True
    )

    replies = []

    query = f"conversation_id:{prediction_tweet_id} -from:PredictionArena"
    
    response = client.search_recent_tweets(
        query=query,
        tweet_fields=["author_id", "created_at", "text"],
        max_results=50
    )

    if not response.data:
        return replies

    for tweet in response.data:
        text = tweet.text.strip().upper()

        if text == "YES" or text == "NO":
            replies.append({
                "tweet_id": tweet.id,
                "author_id": tweet.author_id,
                "answer": text,
                "time": tweet.created_at
            })

    return replies
