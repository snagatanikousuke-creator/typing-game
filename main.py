import sys
import time
import tty
import termios
from engine import GameEngine
from ml_model import TypingMLModel
from word_list import get_word_list
from kana_engine import KanaInputState

TIME_LIMIT = 60  # 秒

def get_single_key() -> str:
    """1キー入力をエコーなしで取得（ターミナル用）"""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch

def show_header():
    print("\033[2J\033[H", end="")  # 画面クリア
    print("=" * 50)
    print("   かな タイピングゲーム  〜 学習型 〜")
    print("=" * 50)
    print("  正解: +10点   ミス（即次の問題）: -3点")
    print(f"  制限時間: {TIME_LIMIT}秒")
    print("=" * 50)

def show_word(word: str, done: str, remaining: str, score: int, time_left: float, current_input: str):
    """問題と入力状況をリアルタイム表示"""
    print(f"\n  残り時間: {time_left:5.1f}秒  |  スコア: {score:4d}点")
    print(f"\n  問題: 【 {word} 】\n")
    # 確定済み（緑）/ 未入力（白）
    print(f"  {done}\033[32m▌\033[0m{remaining}")
    print(f"\n  入力中: {current_input}_", end="", flush=True)

def play_game(engine: GameEngine, model: TypingMLModel, word_list: list[str]):
    engine.start()

    while not engine.is_time_over():
        # ① 問題を出題
        word = model.select_word(word_list)
        model.record_attempt(word)
        state = KanaInputState(word)

        missed_this_word = False

        # ② キー入力ループ（1問）
        while not state.is_complete() and not engine.is_time_over():
            done, remaining = state.get_display()
            print("\033[2J\033[H", end="")  # 画面クリア
            show_word(word, done, remaining, engine.score, engine.time_left(), state.current_input)

            key = get_single_key()

            # Ctrl+C で終了
            if key == "\x03":
                print("\n\n中断しました。")
                return

            # ③ 正誤判定
            result = state.input_key(key)

            if result == "miss":
                # ミスしたかなを記録してすぐ次の問題へ
                seg = state.current_segment()
                if seg:
                    model.record_miss(seg)
                engine.record_miss(word)
                print("\033[2J\033[H", end="")
                print(f"\n  ✗ ミス！  「{word}」  → 次の問題へ")
                time.sleep(0.6)
                missed_this_word = True
                break

        # 完了（時間切れでなく）
        if not missed_this_word and not engine.is_time_over():
            engine.record_correct(word)
            print("\033[2J\033[H", end="")
            print(f"\n  ✓ 正解！  「{word}」  +10点")
            time.sleep(0.4)

    print("\n\n⏰ 時間切れ！")

def show_result(summary: dict):
    print("\n" + "=" * 50)
    print("   ゲーム終了！お疲れさまでした")
    print("=" * 50)
    print(f"  スコア    : {summary['score']:>5} 点")
    print(f"  正解数    : {summary['correct']:>5} 問")
    print(f"  ミス数    : {summary['miss']:>5} 問")
    print(f"  正確率    : {summary['accuracy']:>5.1f} %")
    print("=" * 50)

def main():
    show_header()
    word_list = get_word_list()
    model = TypingMLModel()
    engine = GameEngine(time_limit=TIME_LIMIT)

    input("\nEnterを押してスタート！")

    play_game(engine, model, word_list)

    # ⑤ スコア表示
    summary = engine.get_summary()
    show_result(summary)

    # ⑥ MLモデル更新
    model.update()

    print("\nもう一度プレイしますか？ (y/n): ", end="", flush=True)
    again = input().strip().lower()
    if again == "y":
        main()
    else:
        print("\nまた遊んでね！腕前が上がってるはず！\n")

if __name__ == "__main__":
    main()
