import itertools

ADS_POOL = [
    {
        "id": "jacpot_1",
        "title": "Jacpotfilm — Official",
        "text": "Get the latest videos & exclusive uploads on Jacpotfilm.",
        "button_text": "Visit Jacpotfilm",
        "button_url": "https://t.me/yourchannel"
    },
    {
        "id": "pushpa_promo",
        "title": "Pushpa Specials",
        "text": "Watch Pushpa collection and bonus scenes.",
        "button_text": "Open Pushpa",
        "button_url": "https://t.me/pushpa"
    }
]

_rotator = itertools.cycle(ADS_POOL)

def get_ads_for_query(query: str, max_ads: int = 1):
    q = (query or "").lower().strip()
    selected = []

    if "pushpa" in q:
        selected.append(next(a for a in ADS_POOL if a["id"] == "pushpa_promo"))
    elif "jacpot" in q or "jacpotfilm" in q:
        selected.append(next(a for a in ADS_POOL if a["id"] == "jacpot_1"))
    else:
        for _ in range(max_ads):
            selected.append(next(_rotator))

    return selected[:max_ads]
