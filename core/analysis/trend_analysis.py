from collections import Counter
from typing import Dict, List


def analyze_trends(keywords: List[str]) -> Dict[str, int]:
    return dict(Counter(keywords))
