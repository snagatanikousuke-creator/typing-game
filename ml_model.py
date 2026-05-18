import random
import json
import os
from kana_engine import KANA_PATTERNS

SAVE_PATH = "user_data.json"

class TypingMLModel:
    """
    かな入力に特化した苦手学習モデル。
    キー単位ではなく「かな単位」でミスを記録し、
    苦手なかなを多く含む単語を優先出題する。
    """

    def __init__(self):
        self.miss_count: dict[str, int] = {}   # かなごとのミス回数
        self.total_count: dict[str, int] = {}  # かなごとの出題回数
        self.load()

    def record_miss(self, kana: str):
        """ミスしたかなを記録"""
        self.miss_count[kana] = self.miss_count.get(kana, 0) + 1

    def record_attempt(self, word: str):
        """出題された単語の各かなを出題数としてカウント"""
        for char in word:
            if char in KANA_PATTERNS:
                self.total_count[char] = self.total_count.get(char, 0) + 1

    def get_miss_rate(self) -> dict[str, float]:
        rates = {}
        for kana in self.total_count:
            total = self.total_count[kana]
            miss = self.miss_count.get(kana, 0)
            rates[kana] = miss / total if total > 0 else 0.0
        return rates

    def select_word(self, word_list: list[str]) -> str:
        """苦手なかなを多く含む単語ほど選ばれやすい重み付き選択"""
        miss_rate = self.get_miss_rate()
        weights = []
        for word in word_list:
            score = sum(miss_rate.get(c, 0.3) for c in word if c in KANA_PATTERNS)
            weights.append(max(score, 1.0))
        return random.choices(word_list, weights=weights, k=1)[0]

    def update(self):
        """ゲーム終了後に呼ぶ"""
        self.save()
        self._show_weak_kana()

    def _show_weak_kana(self):
        rates = self.get_miss_rate()
        if not rates:
            print("[ML] まだデータが少ないです。プレイを重ねると苦手分析が始まります。")
            return
        sorted_kana = sorted(rates.items(), key=lambda x: x[1], reverse=True)
        top = [(k, r) for k, r in sorted_kana if r > 0][:5]
        if not top:
            print("[ML] 今回はミスなし！素晴らしい！")
            return
        print("\n[ML] 苦手かな TOP5:")
        for kana, rate in top:
            bar = "█" * int(rate * 10) + "░" * (10 - int(rate * 10))
            # 正しいローマ字も表示
            patterns = KANA_PATTERNS.get(kana, [])
            hint = " / ".join(patterns[:2])
            print(f"  「{kana}」 {bar} {rate*100:.1f}%  ({hint})")

    def save(self):
        data = {"miss_count": self.miss_count, "total_count": self.total_count}
        with open(SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self):
        if os.path.exists(SAVE_PATH):
            with open(SAVE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.miss_count = data.get("miss_count", {})
            self.total_count = data.get("total_count", {})
