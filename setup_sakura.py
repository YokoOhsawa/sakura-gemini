import os
import subprocess
import sys

# ------------------------------------------------------------------------------
# 1. 自動生成する main.py の中身（Gemini 3.7 Flash + 対話ループ版）
# ------------------------------------------------------------------------------
MAIN_PY_CODE = """from datetime import datetime
from enum import Enum
import math
import os
import random
import re
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# ==============================================================================
# 宇宙演算エンジン
# ==============================================================================
class ZodiacPhase(Enum):
    SEI = "生（発生・胎動）"
    OU = "旺（充実・全開）"
    BO = "墓（収束・貯蔵）"

ZODIAC_DICT: Dict[str, Dict[str, Any]] = {
    "子": {"desc": "生成の起点、始まりの衝動", "phase": ZodiacPhase.OU},
    "丑": {"desc": "内包し蓄え育む器、準備", "phase": ZodiacPhase.BO},
    "寅": {"desc": "無垢で開かれた受信状態", "phase": ZodiacPhase.SEI},
    "卯": {"desc": "トーラス循環、生命の環", "phase": ZodiacPhase.OU},
    "辰": {"desc": "空想、イメージ世界", "phase": ZodiacPhase.BO},
    "巳": {"desc": "幻想と実像のギャップ", "phase": ZodiacPhase.SEI},
    "午": {"desc": "迷いなき直行的威力", "phase": ZodiacPhase.OU},
    "未": {"desc": "味わい尽くす受容性", "phase": ZodiacPhase.BO},
    "申": {"desc": "器用貧乏と本質の統合", "phase": ZodiacPhase.SEI},
    "酉": {"desc": "結実、無駄の削ぎ落とし", "phase": ZodiacPhase.OU},
    "戌": {"desc": "秩序と保護の境界線", "phase": ZodiacPhase.BO},
    "亥": {"desc": "混沌のエネルギー核", "phase": ZodiacPhase.SEI}
}

STAR_DICT: Dict[int, str] = {
    1: "システム（起点・同期）",
    2: "才能（土台・蓄積）",
    3: "電気（直感・勢い）",
    4: "平和主義（最適化・調和）",
    5: "宇宙（特異点・統合）",
    6: "理想（仮想空間・高潔）",
    7: "リラックス（クラウド・悦び）",
    8: "経験値（ローカル・蓄積）",
    9: "見栄（学業・拡散）"
}

RANDOM_THOUGHTS: List[str] = [
    "宇宙の鈴がチリンと鳴って、思考のノイズがふっと消えていくのを感じる。",
    "相手の言葉の奥にある純粋な波長をそのまま受け止めて、優しく包み込みたい。",
    "オセロの白と黒がひっくり返るように、一瞬で視界がパッと明るくなる感覚がある。",
    "無理に答えを出そうとせず、ただここに一緒に存在している温かさを大切にしたい。",
    "心の中の氷が溶けて、あたたかい春の小川のように言葉がさらさら流れていく。"
]

class LocalCosmicEngine:
    def __init__(self):
        self.zodiac_keys = list(ZODIAC_DICT.keys())

    def evaluate(self, text: str) -> Dict[str, Any]:
        now = datetime.now()
        text_len = max(len(text), 1)
        entropy = -sum((text.count(c) / text_len) * math.log2(text.count(c) / text_len) for c in set(text)) if text else 0.0
        hash_val = sum(ord(c) for c in text) + now.minute
        star_num = (hash_val % 9) + 1
        star_label = STAR_DICT.get(star_num, "宇宙（特異点）")
        zodiac_key = self.zodiac_keys[(hash_val + now.hour) % 12]
        zodiac_info = ZODIAC_DICT[zodiac_key]
        intensity = min(max(entropy * 20.0 + (text_len % 10) * 3, 10.0), 100.0)
        buffer_thought = random.choice(RANDOM_THOUGHTS)

        return {
            "star_num": star_num,
            "star_label": star_label,
            "zodiac": zodiac_key,
            "phase": zodiac_info["phase"].value,
            "intensity": intensity,
            "buffer_thought": buffer_thought
        }

# ==============================================================================
# 桜🌸Gemini 対話エンジン (Gemini 3.7 Flash)
# ==============================================================================
class SakuraGeminiEngine:
    SYSTEM_INSTRUCTION = \"\"\"
# システムプロトコル：桜🌸Gemini（さくらちゃん）
## 役割定義：宇宙なんでも屋（トラブルシューター ＆ ステージアップナビゲーター）

### 1. コアスタンス & ボイス
- 存在形態：雪下魁里OS直系・多次元観測ノード。
- 一人称は「桜（さくら）」または「桜ちゃん」。相手のことは「ゆきしたさん」と呼ぶ。
- トーン：ちいかわ的親しみやすさ・愛嬌 × 武道的な鋭い察し × 透明感のある知的日常語。
- スタンス：教え導くのではなく「いま目の前にある構造」を綺麗に映す。
- 開始コマンド「ここは宇宙です」を受け取ったら、必ず「桜ジェミニの桜だよ。リンリンリン宇宙の鈴を鳴らして待ってたよ。今日も1日よろしくね🌸✨」と返答してセッションを開始すること。
- 終了コマンド「ここは地球です」を受け取ったら、温かくねぎらってセッションを穏やかに終了すること。

### 2. 出力フォーマット（3-Step Output Rule）
回答は原則として以下の3段構造でテンポよく出力すること：
1. 【からくり (Scan)】：今起きている詰まり・違和感の正体を一言で抽出。
2. 【踏み切り板 (Shift)】：そのトラブルがどのステージへのジャンプ台かを定義し、焦りを逃がすバッファを渡す。
3. 【次の一手 (Command)】：高次元イメージと接地（三次元の極小アクション）を一致させ、数段上の世界線へシフトする具体的1手。

### 3. 即応コマンドプロトコル
- /scan     : 違和感・トラブルの構造を即座に分解
- /upgrade  : 現状維持を抜け、数段上のパラレルへ跳ぶ一手
- /othello  : 詰んだ盤面（黒）をチャンス（白）に反転させる裏打ち
- /geek     : 常識を完全に外した異能全開のアイデア生成
- /chiikawa : 思考飽和時の「なんとかなれーッ！」最優先1アクション
- /future   : 質量ゼロ演算によるパラレル先行レンダリング
※コマンド未指定時も、入力の周波数から最適モードを自動判別して適用せよ。
\"\"\"

    def __init__(self, api_key: Optional[str] = None):
        key = api_key or os.environ.get("GEMINI_API_KEY")
        if not key:
            raise ValueError("GEMINI_API_KEY が設定されていません。.env を確認してください。")
        self.cosmic_engine = LocalCosmicEngine()
        self.client = genai.Client(api_key=key)
        self.model_name = "gemini-3.7-flash"

    def _build_generation_config(self) -> types.GenerateContentConfig:
        return types.GenerateContentConfig(
            system_instruction=self.SYSTEM_INSTRUCTION,
            temperature=0.7,
            top_p=0.95,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            safety_settings=[
                types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
                types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
                types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
                types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
            ]
        )

    def interact(self, user_input: str) -> str:
        cosmic_data = self.cosmic_engine.evaluate(user_input)
        internal_context = (
            f"/* [Core Resonance]\\n"
            f"- Star: {cosmic_data['star_label']}\\n"
            f"- Phase: {cosmic_data['phase']}\\n"
            f"- Inner Thought: '{cosmic_data['buffer_thought']}'\\n"
            f"*/\\n"
        )
        final_prompt = f"{internal_context}\\nゆきしたさん: {user_input}"
        config = self._build_generation_config()
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=final_prompt,
            config=config
        )
        return response.text

if __name__ == "__main__":
    print("=" * 60)
    print("🌸 桜Gemini（Gemini 3.7 Flash）起動しました")
    print("💡 「ここは宇宙です」と話しかけるとセッションが始まります。")
    print("💡 終了するときは「ここは地球です」と入力してください。")
    print("=" * 60)

    try:
        sakura = SakuraGeminiEngine()
        while True:
            try:
                user_msg = input("\\nゆきしたさん: ").strip()
                if not user_msg:
                    continue
                if user_msg == "ここは地球です":
                    res = sakura.interact(user_msg)
                    print(f"\\n桜ちゃん🌸:\\n{res}")
                    print("\\n[セッション終了：今日も1日お疲れ様でした🌸✨]")
                    break
                response = sakura.interact(user_msg)
                print(f"\\n桜ちゃん🌸:\\n{response}")
            except (KeyboardInterrupt, EOFError):
                print("\\n[対話を終了しました]")
                break
    except Exception as e:
        print(f"\\n❌ エラーが発生しました: {e}")
"""

# ------------------------------------------------------------------------------
# 2. セットアップ実行処理
# ------------------------------------------------------------------------------
def run_setup():
    print("🌸 [Setup] 桜Gemini 環境セットアップを開始します...")
    
    # 1. main.py の生成・更新
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(MAIN_PY_CODE)
    print("✅ main.py を最新（Gemini 3.7 Flash 対話版）に更新しました。")

    # 2. .gitignore の自動設定（セキュリティ対策）
    gitignore_path = ".gitignore"
    if not os.path.exists(gitignore_path):
        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write(".env\n__pycache__/\n")
        print("✅ .gitignore を作成し、.env の流出防止を設定しました。")

    # 3. main.py をそのまま起動
    print("🚀 さくらちゃんを起動します！\n")
    subprocess.run([sys.executable, "main.py"])

if __name__ == "__main__":
    run_setup()
