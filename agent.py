# agent.py

import os
import time
import json
import hashlib
import tweepy

from collector import collect_posts
from signals import detect_signals
from interpretations import interpret_signal
from reporter import generate_report

STATE_FILE = "state.json"
SLEEP_SECONDS = 180  # 3 minutes


# ---------- STATE HELPERS ----------

def load_state():
    if not os.path.exists(STATE_FILE):
        return {
            "active_prediction_id": None,
            "last_signal_hash": None
        }
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


# ---------- MAIN LOOP ----------

def main():
    client = tweepy.Client(
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_SECRET"),
        bearer_token=os.getenv("X_BEARER_TOKEN"),
        wait_on_rate_limit=True
    )

    state = load_state()

    # 1️⃣ collect posts
    posts = collect_posts()
    if not posts:
        print("no posts collected. staying silent.")
        return

    # 2️⃣ detect signals
signals = detect_signals(posts)

if not signals or not isinstance(signals, list):
    print("no valid signals returned:", signals)
    return

signal = signals[0]

    # use the strongest / first signal
    signal = signals[0]

    # 3️⃣ prevent duplicate predictions
    signal_hash = hashlib.sha256(str(signal).encode()).hexdigest()

    if state["last_signal_hash"] == signal_hash:
        print("signal already processed. skipping.")
        return

    if state["active_prediction_id"] is not None:
        print("prediction already active. waiting for resolution.")
        return

    # 4️⃣ interpret signal
    interpretation = interpret_signal(signal)
    if not interpretation:
        print("signal not strong enough to interpret.")
        return

    # 5️⃣ generate prediction tweet
    prediction_tweet = generate_report(interpretation)
    if not prediction_tweet:
        print("empty prediction text. aborting.")
        return

    # 6️⃣ post prediction
    response = client.create_tweet(text=prediction_tweet)
    prediction_id = response.data["id"]

    # 7️⃣ save state
    state["active_prediction_id"] = prediction_id
    state["last_signal_hash"] = signal_hash
    save_state(state)

    print("prediction stored for resolution:", prediction_id)


# ---------- RUN FOREVER ----------

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print("error:", e)

        time.sleep(SLEEP_SECONDS)
