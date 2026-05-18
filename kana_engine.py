# かな入力エンジン
# ひらがな1文字（または2文字の拗音）に対して
# 有効なローマ字入力パターンを全て定義し、
# プレフィックスマッチングでリアルタイム判定する

# ひらがな → 有効ローマ字パターンのリスト
KANA_PATTERNS: dict[str, list[str]] = {
    # あ行
    "あ": ["a"],
    "い": ["i", "yi"],
    "う": ["u", "wu"],
    "え": ["e"],
    "お": ["o"],
    # か行
    "か": ["ka", "ca"],
    "き": ["ki"],
    "く": ["ku", "cu", "qu"],
    "け": ["ke"],
    "こ": ["ko", "co"],
    # さ行
    "さ": ["sa"],
    "し": ["si", "shi", "ci"],
    "す": ["su"],
    "せ": ["se", "ce"],
    "そ": ["so"],
    # た行
    "た": ["ta"],
    "ち": ["ti", "chi"],
    "つ": ["tu", "tsu"],
    "て": ["te"],
    "と": ["to"],
    # な行
    "な": ["na"],
    "に": ["ni"],
    "ぬ": ["nu"],
    "ね": ["ne"],
    "の": ["no"],
    # は行
    "は": ["ha"],
    "ひ": ["hi"],
    "ふ": ["fu", "hu"],
    "へ": ["he"],
    "ほ": ["ho"],
    # ま行
    "ま": ["ma"],
    "み": ["mi"],
    "む": ["mu"],
    "め": ["me"],
    "も": ["mo"],
    # や行
    "や": ["ya"],
    "ゆ": ["yu"],
    "よ": ["yo"],
    # ら行
    "ら": ["ra"],
    "り": ["ri"],
    "る": ["ru"],
    "れ": ["re"],
    "ろ": ["ro"],
    # わ行
    "わ": ["wa"],
    "ゐ": ["wi"],
    "ゑ": ["we"],
    "を": ["wo"],
    # ん
    "ん": ["nn", "xn"],
    # が行
    "が": ["ga"],
    "ぎ": ["gi"],
    "ぐ": ["gu"],
    "げ": ["ge"],
    "ご": ["go"],
    # ざ行
    "ざ": ["za"],
    "じ": ["zi", "ji"],
    "ず": ["zu"],
    "ぜ": ["ze"],
    "ぞ": ["zo"],
    # だ行
    "だ": ["da"],
    "ぢ": ["di"],
    "づ": ["du"],
    "で": ["de"],
    "ど": ["do"],
    # ば行
    "ば": ["ba"],
    "び": ["bi"],
    "ぶ": ["bu"],
    "べ": ["be"],
    "ぼ": ["bo"],
    # ぱ行
    "ぱ": ["pa"],
    "ぴ": ["pi"],
    "ぷ": ["pu"],
    "ぺ": ["pe"],
    "ぽ": ["po"],
    # 小文字・特殊
    "ぁ": ["la", "xa"],
    "ぃ": ["li", "xi"],
    "ぅ": ["lu", "xu"],
    "ぇ": ["le", "xe"],
    "ぉ": ["lo", "xo"],
    "っ": ["ltu", "xtu", "ltsu", "xtsu"],
    "ゃ": ["lya", "xya"],
    "ゅ": ["lyu", "xyu"],
    "ょ": ["lyo", "xyo"],
    "ー": ["-"],
    # 拗音（きゃ行）
    "きゃ": ["kya"],
    "きぃ": ["kyi"],
    "きゅ": ["kyu"],
    "きぇ": ["kye"],
    "きょ": ["kyo"],
    # しゃ行
    "しゃ": ["sya", "sha"],
    "しぃ": ["syi"],
    "しゅ": ["syu", "shu"],
    "しぇ": ["sye", "she"],
    "しょ": ["syo", "sho"],
    # ちゃ行
    "ちゃ": ["tya", "cha"],
    "ちぃ": ["tyi"],
    "ちゅ": ["tyu", "chu"],
    "ちぇ": ["tye", "che"],
    "ちょ": ["tyo", "cho"],
    # にゃ行
    "にゃ": ["nya"],
    "にぃ": ["nyi"],
    "にゅ": ["nyu"],
    "にぇ": ["nye"],
    "にょ": ["nyo"],
    # ひゃ行
    "ひゃ": ["hya"],
    "ひぃ": ["hyi"],
    "ひゅ": ["hyu"],
    "ひぇ": ["hye"],
    "ひょ": ["hyo"],
    # みゃ行
    "みゃ": ["mya"],
    "みぃ": ["myi"],
    "みゅ": ["myu"],
    "みぇ": ["mye"],
    "みょ": ["myo"],
    # りゃ行
    "りゃ": ["rya"],
    "りぃ": ["ryi"],
    "りゅ": ["ryu"],
    "りぇ": ["rye"],
    "りょ": ["ryo"],
    # ぎゃ行
    "ぎゃ": ["gya"],
    "ぎぃ": ["gyi"],
    "ぎゅ": ["gyu"],
    "ぎぇ": ["gye"],
    "ぎょ": ["gyo"],
    # じゃ行
    "じゃ": ["zya", "ja", "jya"],
    "じぃ": ["zyi", "jyi"],
    "じゅ": ["zyu", "ju", "jyu"],
    "じぇ": ["zye", "je", "jye"],
    "じょ": ["zyo", "jo", "jyo"],
    # びゃ行
    "びゃ": ["bya"],
    "びぃ": ["byi"],
    "びゅ": ["byu"],
    "びぇ": ["bye"],
    "びょ": ["byo"],
    # ぴゃ行
    "ぴゃ": ["pya"],
    "ぴぃ": ["pyi"],
    "ぴゅ": ["pyu"],
    "ぴぇ": ["pye"],
    "ぴょ": ["pyo"],
    # ふゃ行
    "ふぁ": ["fa"],
    "ふぃ": ["fi"],
    "ふぇ": ["fe"],
    "ふぉ": ["fo"],
}

def build_prefix_set(patterns: list[str]) -> set[str]:
    """パターンの全プレフィックスをセットで返す"""
    prefixes = set()
    for p in patterns:
        for i in range(1, len(p) + 1):
            prefixes.add(p[:i])
    return prefixes


def precompute():
    """
    全かなについて (パターンセット, プレフィックスセット) を事前計算。
    拗音（2文字かな）は先に処理する必要があるので別管理。
    """
    result = {}
    for kana, patterns in KANA_PATTERNS.items():
        result[kana] = {
            "patterns": set(patterns),
            "prefixes": build_prefix_set(patterns),
        }
    return result

KANA_DATA = precompute()

# 2文字かな（拗音）を先に判定するためのリスト
TWO_CHAR_KANA = [k for k in KANA_PATTERNS if len(k) == 2]


class KanaInputState:
    """
    1単語の入力状態を管理するクラス。
    word: ひらがな文字列（例: "にほんご"）
    """

    def __init__(self, word: str):
        self.word = word
        self.segments = self._split_to_segments(word)  # ["に","ほ","ん","ご"]
        self.seg_index = 0      # 今何文字目か
        self.current_input = "" # 現在の文字に対して入力中のローマ字
        self.missed_keys: list[str] = []  # ミスしたキー記録

    def _split_to_segments(self, word: str) -> list[str]:
        """
        ひらがな文字列を入力単位（セグメント）に分割。
        拗音（きゃ等）は2文字で1セグメント。
        っの後続子音二重打ちも考慮。
        """
        segments = []
        i = 0
        while i < len(word):
            # 2文字拗音チェック
            if i + 1 < len(word) and (word[i] + word[i+1]) in KANA_PATTERNS:
                segments.append(word[i] + word[i+1])
                i += 2
            else:
                segments.append(word[i])
                i += 1
        return segments

    def current_segment(self):
        if self.seg_index < len(self.segments):
            return self.segments[self.seg_index]
        return None

    def is_complete(self) -> bool:
        return self.seg_index >= len(self.segments)

    def input_key(self, key: str) -> str:
        """
        1キー入力を受け取り結果を返す。
        戻り値: "correct"（1文字確定）| "pending"（入力途中）| "miss"（ミス）
        """
        seg = self.current_segment()
        if seg is None:
            return "correct"

        data = KANA_DATA.get(seg)
        if data is None:
            return "miss"

        # ん の特殊処理: n + 次の文字の子音 で確定（例: んご → ngo の n で確定）
        if seg == "ん" and self.current_input == "n":
            next_seg = self.segments[self.seg_index + 1] if self.seg_index + 1 < len(self.segments) else None
            if next_seg:
                next_data = KANA_DATA.get(next_seg)
                # 次の文字の先頭が n 以外の子音なら「ん」確定
                if next_data and key != "n" and key != "a" and key != "i" and key != "u" and key != "e" and key != "o":
                    self.current_input = ""
                    self.seg_index += 1
                    # そのキーを次の文字の入力として再処理
                    self.current_input = key
                    if key in KANA_DATA.get(next_seg, {}).get("prefixes", set()):
                        return "correct"  # んが確定（次の文字はまだpending）
                    else:
                        return "correct"

        # っの特殊処理: 次の文字の子音を2回打つパターン（例: っか → kka）
        if seg == "っ" and self.seg_index + 1 < len(self.segments):
            next_seg = self.segments[self.seg_index + 1]
            next_data = KANA_DATA.get(next_seg)
            if next_data:
                for pattern in next_data["patterns"]:
                    if pattern and key == pattern[0]:
                        # っ確定、次の文字の入力開始
                        self.missed_keys  # 記録なし（正解）
                        self.seg_index += 1
                        self.current_input = key
                        return "correct"

        new_input = self.current_input + key

        # 完全一致チェック
        if new_input in data["patterns"]:
            self.current_input = ""
            self.seg_index += 1
            return "correct"

        # プレフィックスチェック（まだ途中の可能性あり）
        if new_input in data["prefixes"]:
            self.current_input = new_input
            return "pending"

        # どのパターンにもマッチしない → ミス
        self.missed_keys.append(key)
        return "miss"

    def get_display(self):
        """
        表示用に（確定済み部分, 未入力部分）を返す。
        """
        done = "".join(self.segments[:self.seg_index])
        remaining = "".join(self.segments[self.seg_index:])
        return done, remaining
