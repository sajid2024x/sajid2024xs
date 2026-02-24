# interpretations.py

def interpret_signal(signal):
    if not signal:
        return None

    keyword = signal["keyword"]
    count = signal["count"]
    accounts = signal["accounts"]

    if count >= 5:
        strength = "strong"
    elif count >= 3:
        strength = "moderate"
    else:
        return None  # too weak to report

    interpretation = {
        "summary": (
            f'{count} monitored agents mentioned "{keyword}" '
            f'in a short time window.'
        ),
        "analysis": (
            f'this looks like a {strength} narrative forming, '
            f'possibly coordinated or reactive.'
        ),
        "accounts": accounts,
        "keyword": keyword,
        "strength": strength
    }

    return interpretation
