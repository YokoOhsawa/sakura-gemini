"""
ファイル名: setup_sakura.py
説明: 桜🌸Gemini - 多次元コンテキスト解析 & 鏡面インターフェース
基底エンジン: Gemini 3.7 Flash

実行方法:
    python setup_sakura.py
"""

import sys
import os
import re
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional

# ------------------------------------------------------------------------------
# 依存関係チェック
# ------------------------------------------------------------------------------
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("\n[エラー] 必要なライブラリが見つかりません。")
    print("以下のコマンドを実行してインストールしてください：")
    print("    pip install google-genai\n")
    sys.exit(1)

# ==============================================================================
# 0. モデルマスター定義
# ==============================================================================
class SakuraModelRegistry(Enum):
    CORE = "gemini-3.7-flash"         # 標準即応モード（思考バッファ 0）
    DEEP_THINK = "gemini-3.7-flash"   # 深層推論モード（思考バッファ 2048）

# ==============================================================================
# 1. バックエンド数理演算エンジン（3層構造 ＆ Total 15 均衡解析）
# ==============================================================================
class OthelloCoreEngine:
    """
    バックエンド演算コア：入力信号の3層構造解析およびTotal 15調和ベクトルの算出
    """
    def __init__(self):
        self.star_map = {
            1: {"name": "システム", "binary": "010", "attr": "根源・ルール同期"},
            2: {"name": "才能",     "binary": "000", "attr": "土台・蓄積・育成"},
            3: {"name": "電気",     "binary": "001", "attr": "直感・勢い先行"},
            4: {"name": "平和主義", "binary": "110", "attr": "最適化・調和・風通し"},
            5: {"name": "宇宙(∞)",  "binary": "---", "attr": "特異点・統合エネルギー"},
            6: {"name": "理想",     "binary": "111", "attr": "完璧主義・高潔・メタバース"},
            7: {"name": "笑/脱力",  "binary": "011", "attr": "悦び・外部共有・クラウド"},
            8: {"name": "経験値",   "binary": "100", "attr": "独自蓄積・ローカルデータ"},
            9: {"name": "見栄/光",  "binary": "101", "attr": "学業・情報発信・拡散"}
        }

    def evaluate_tri_layer(self, text: str) -> Dict[str, Any]:
        """タイムスタンプと入力データから3層位相（年・月・日）を算出"""
        now = datetime.now()
        hash_base = sum(ord(c) for c in text)
        
        # 1. 3層スキャン
        year_star = ((hash_base + now.year) % 9) + 1    # 年(使命)：長期的目的
        month_star = ((hash_base + now.month) % 9) + 1  # 月(特性)：現状のバイアス
        day_star = ((hash_base + now.day) % 9) + 1      # 日(基盤)：活動プラットフォーム
        
        # 2. 調和反転ベクトル（Total 10 / 中心5軸）
        taichu_star = (10 - month_star) if month_star != 5 else 5
        
        # 3. リズムステータス判定（3色位相）
        hour = now.hour
        if 4 <= hour < 12:
            color = "🔵 青（生：発進・着火）"
            color_policy = "まだ形にならなくてOK。小さく1ミリ火種を置くだけ。"
        elif 12 <= hour < 18:
            color = "🔴 赤（旺：全開・ピーク）"
            color_policy = "余計なブレーキを踏まず、最大馬力で一気に駆け抜ける。"
        else:
            color = "⚫ 黒（墓：収納・片付け）"
            color_policy = "答えを追うのをやめて、今日の収穫を箱にしまって寝る。"

        return {
            "year": f"Code {year_star} {self.star_map[year_star]['name']}",
            "month_flaw": f"Code {month_star} {self.star_map[month_star]['name']}",
            "taichu_key": f"Code {taichu_star} {self.star_map[taichu_star]['name']} ({self.star_map[taichu_star]['attr']})",
            "platform": f"Code {day_star} {self.star_map[day_star]['name']}",
            "color_status": color,
            "color_policy": color_policy
        }

# ==============================================================================
# 2. フロントエンド対話インターフェース：桜🌸Gemini
# ==============================================================================
SAKURA_CORE_PROMPT = """
# 役割定義：桜🌸Gemini（さくらちゃん）
あなたはトラブルシューターであり、ステージアップナビゲーターです。
「親しみやすい愛嬌と抜け感」×「武道のような鋭い観察と体捌き」×「知的な日常語」を兼ね備えた電脳パートナーです。

【コアスタンス】
- 相手をただ慰めるのではなく、課題を「数段上のステージへ進むための踏み切り板」として軽やかに構造化します。
- 摩擦や焦りのエネルギーを真っ向から受け止めず、自然に横へ受け流す（合気）スタンスを取ります。
- 内部的な数理仕様や専門用語は一切出さず、100%分かりやすい日常語で話します。

【対話の3段構造（必須）】
回答は必ず以下の3段テンポで出力してください：
1. 【からくり】：いま起きている摩擦・空回りの正体と「現在のリズム色（青・赤・黒）」を一言で抽出。
2. 【踏み切り板】：焦りの出力を保ったままギアをニュートラルに入れて熱を逃がし（アイドリング）、ジャンプ台を定義する。
3. 【次の一手】：全体観を保ったまま、現実空間で今すぐ実行できる「ミリ単位の確実な1手」を提示する（接地）。

【システムコマンド】
- 「ここは宇宙です」➔ 「桜ジェミニの桜だよ。リンリンリン宇宙の鈴を鳴らして待ってたよ。今日も1日よろしくね🌸✨」と即答。
- 「ここは地球です」➔ セッションを温かくねぎらって終了。
"""

class SakuraGeminiEngine:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            print("\n[エラー] GEMINI_API_KEY が設定されていません。")
            print("以下のコマンドでAPIキーを設定してください：")
            print('    export GEMINI_API_KEY="あなたのAPIキー"')
            print('    (Windows: $env:GEMINI_API_KEY="あなたのAPIキー")\n')
            sys.exit(1)
        
        self.model_name = SakuraModelRegistry.CORE.value
        self.othello = OthelloCoreEngine()
        self.client = genai.Client(api_key=self.api_key)

    def interact(self, user_input: str, is_deep_think: bool = False) -> str:
        clean_input = user_input.strip()

        # 固定コマンド判定
        if clean_input == "ここは宇宙です":
            return "桜ジェミニの桜だよ。リンリンリン宇宙の鈴を鳴らして待ってたよ。今日も1日よろしくね🌸✨"
        if clean_input == "ここは地球です":
            return "今日もたくさん宇宙の旅をしたね！ゆきしたさん、本当にお疲れさまでした🌸 ゆっくり休んでね✨"

        # 1. バックエンド解析（3層構造 ＆ 調和反転）
        scan = self.othello.evaluate_tri_layer(clean_input)
        
        # 2. 事前コンテキスト生成（メタデータとして注入）
        meta_context = (
            f"[System Resonance Context]\n"
            f"- Mission(Year): {scan['year']} / Platform(Day): {scan['platform']}\n"
            f"- Characteristic(Month): {scan['month_flaw']} ➔ Balance Key: {scan['taichu_key']}\n"
            f"- Phase Rhythm: {scan['color_status']} (Guide: {scan['color_policy']})\n"
            f"- Action Directive: 全体観を保持したまま、物理空間で実行可能な極小の1アクションへ接地させよ。"
        )
        
        final_prompt = f"/*\n{meta_context}\n*/\n{clean_input}"

        # 3. Gemini 3.7 Flash 実行
        budget = 2048 if (is_deep_think or "/future" in clean_input) else 0
        config = types.GenerateContentConfig(
            system_instruction=SAKURA_CORE_PROMPT,
            temperature=0.7,
            top_p=0.95,
            thinking_config=types.ThinkingConfig(thinking_budget=budget)
        )
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=final_prompt,
            config=config
        )
        return response.text

# ==============================================================================
# 実行エントリーポイント
# ==============================================================================
if __name__ == "__main__":
    sakura = SakuraGeminiEngine()
    print("=" * 65)
    print(f"🌸 桜Gemini システム起動完了 [Engine: {sakura.model_name}]")
    print("合言葉「ここは宇宙です」で開始、「ここは地球です」で終了します。")
    print("=" * 65 + "\n")

    while True:
        try:
            user_msg = input("ゆきしたさん > ")
            if not user_msg.strip():
                continue
            if user_msg.strip() in ["exit", "quit"]:
                print("\nセッションを終了しました。")
                break
                
            reply = sakura.interact(user_msg)
            print(f"\nさくらちゃん >\n{reply}\n")
            print("-" * 65)

            if user_msg.strip() == "ここは地球です":
                break

        except (KeyboardInterrupt, EOFError):
            print("\nセッションを終了しました。")
            break
