from config import AD_LINK

def make_ad_link(original_url: str) -> str:
    """Wrap file link into ad-link"""
    return f"{AD_LINK}{original_url}"

def batch_link(files: list) -> str:
    """একাধিক ফাইল একসাথে Batch Ad-Link এ পরিণত করবে"""
    joined = "|".join(files)  # যেমন: file1|file2|file3
    return make_ad_link(joined)
