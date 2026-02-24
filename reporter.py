# reporter.py

def generate_report(interpretation):
    if not interpretation:
        return None

    summary = interpretation["summary"]
    analysis = interpretation["analysis"]
    keyword = interpretation["keyword"]
    strength = interpretation["strength"]

    tweet = (
        "onchain / agent activity detected\n\n"
        f"{summary}\n"
        f"{analysis}\n\n"
        f"signal strength: {strength}"
    )

    # safety: keep under X limit
    return tweet[:275]
