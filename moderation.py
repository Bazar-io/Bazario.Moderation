from pathlib import Path
from typing import List, Dict
import pandas as pd

DATA_XLSX = Path(__file__).with_name("okak.xlsx")
try:
    WORDS: List[str] = (
        pd.read_excel(DATA_XLSX, engine="openpyxl")
        .iloc[:, 0].dropna().astype(str).str.lower().tolist()
    )
except Exception as exc:
    print(f"[ERROR] {DATA_XLSX}: {exc}")
    WORDS = []
try:
    from Levenshtein import distance as lv_distance
except ImportError:
    def lv_distance(a: str, b: str) -> int:
        n, m = len(a), len(b)
        if n > m:
            a, b, n, m = b, a, m, n
        current = list(range(n + 1))
        for i in range(1, m + 1):
            prev, current = current, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = prev[j] + 1, current[j - 1] + 1, prev[j - 1]
                if a[j - 1] != b[i - 1]:
                    change += 1
                current[j] = min(add, delete, change)
        return current[n]
SYMBOL_MAP = {
    'a': ['a', '@', '4'],     'b': ['b', '6', '8'],
    'c': ['c', 'ć'],          'd': ['d'],
    'e': ['e', '3'],          'f': ['f'],
    'g': ['g', '9'],          'h': ['h'],
    'i': ['i', '1', '!', '|'],'j': ['j'],
    'k': ['k'],               'l': ['l', '1', '|'],
    'm': ['m'],               'n': ['n', 'ń'],
    'o': ['o', '0'],          'p': ['p'],
    'q': ['q'],               'r': ['r'],
    's': ['s', '$', 'ś'],     't': ['t', '7'],
    'u': ['u', 'v'],          'v': ['v', 'u'],
    'w': ['w'],               'x': ['x'],
    'y': ['y'],               'z': ['z', 'ż', 'ź', '2'],
    'ą': ['ą'], 'ć': ['ć'], 'ę': ['ę'], 'ł': ['ł'],
    'ń': ['ń'], 'ó': ['ó', 'o', '0'], 'ś': ['ś'],
    'ź': ['ź'], 'ż': ['ż'],
}

REVERSE_MAP = {sym: base for base, lst in SYMBOL_MAP.items() for sym in lst}

def _normalize(text: str) -> str:
    return ''.join(REVERSE_MAP.get(ch, ch) for ch in text.lower() if ch != ' ')

def detect_banned_words(text: str) -> List[Dict[str, str]]:
    phrase = _normalize(text)
    detected = []

    for word in WORDS:
        wl = len(word)
        max_dist = int(wl * 0.25)
        for i in range(len(phrase) - wl + 1):
            frag = phrase[i : i + wl]
            if lv_distance(frag, word) <= max_dist:
                detected.append(
                    {"banedWord": word, "similarWords": frag}
                )
    return detected
