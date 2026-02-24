# reporter.py

def generate_report(signal):
    keyword = signal["keyword"]
    count = signal["count"]
    accounts = ", ".join(signal["accounts"])

    report = (
        f"{count} monitored accounts mentioned '{keyword}' "
        f"within a short time window.\n\n"
        f"Accounts involved: {accounts}\n\n"
        f"Possible coordinated narrative forming."
    )

    return report
