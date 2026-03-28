import re
import sys

def score_chill_factor(path="story.md"):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    words = len(text.split())
    active_verbs = len(re.findall(r'\b(chase|slam|whisper|creep|stare|grab|tear|spin|back away|flicker|stretch|laugh|flash|reach|type|hammer|rattle|soak|smile|bleed|wait|watch)\b', text, re.IGNORECASE))
    tension_words = len(re.findall(r'\b(pulse|dread|shadow|wet copper|knife|bleeding|mirror|eyes wrong|too late|finish the story|the end|unreliable|forgotten|buried|returned)\b', text, re.IGNORECASE))
    cliffhanger = 2 if re.search(r'\?$|\.\.\.$|anymore\.?$|left bleeding\.?$|fingers weren\'t mine', text.splitlines()[-1].strip(), re.IGNORECASE) else 0

    over_limit = -1 if words > 2000 else 0
    cliche_penalty = -2 * len(re.findall(r'\b(heart raced|eyes widened|heart pounded)\b', text, re.IGNORECASE))

    raw_score = active_verbs + tension_words + cliffhanger + over_limit + cliche_penalty
    normalized = raw_score / max(1, words / 150)
    return normalized

if __name__ == "__main__":
    score = score_chill_factor()
    print(f"CHILL_FACTOR:{score:.3f}")
    sys.exit(0)