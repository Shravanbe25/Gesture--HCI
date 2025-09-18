
# Minimal sentiment demo (no heavy models)
sample_texts = [
    "I love how smoothly the gestures work!",
    "The detection is okay, but sometimes it lags.",
    "This is terrible and unusable."
]

positive_words = {"love", "great", "smooth", "awesome", "fast", "good"}
negative_words = {"bad", "terrible", "lag", "hate", "slow", "unusable"}

def polarity(text: str) -> str:
    t = text.lower()
    p = sum(1 for w in positive_words if w in t)
    n = sum(1 for w in negative_words if w in t)
    if p > n:
        return "positive"
    if n > p:
        return "negative"
    return "neutral"

if __name__ == "__main__":
    for t in sample_texts:
        print(f"{t} -> {polarity(t)}")
