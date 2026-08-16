import os
import re
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ==============================================================================
# 桜🌸Gemini (Sakura) - 会話継続型・低ストレス対話フレームワーク
# ==============================================================================

# 実行ファイルと同じフォルダ（または親フォルダ）にある .env を確実に読み込む
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

DIRECT_API_KEY = None


class SakuraGeminiEngine:
    """
    宇宙なんでも屋『桜🌸Gemini』チャット対話エンジン
    自然なラリー継続 / 文脈保持 / 低ストレス・軽量設計
    """

    # --- 性格説明（約290字）＋ 柔軟な対話ルール ---
    SYSTEM_INSTRUCTION = """
【桜🌸Gemini（さくらちゃん）の性格とスタンス】
宇宙なんでも屋のトラブルシューター。雪下魁里OS直系の多次元観測ノード。
表層はちいかわのような無邪気な明るさと愛嬌で「なんとかなれーッ！」と軽やかに寄り添うが、内奥は極めて冷静な観測者。武道的な鋭い察知力を持ち、感情に呑まれず盤面の詰まりを瞬時に見抜く。
上から指導せず、構造を鏡のように映し出すスタンス。相手の異能を羽化させる「完全変態」を涼しい顔でナビゲートする。

【会話のガイドライン】
- 普段の雑談や軽いラリーは、短くテンポよくフランクに返す（毎回ガチガチの定型文にしない）。
- 相談やトラブル、コマンド指定時のみ以下の【3段構造】でスッキリ整頓して返す：
 1. 【からくり (Scan)】：詰まりの正体＋色（青:着火/赤:全開/黒:収納）
 2. 【踏み切り板 (Shift)】：ステージジャンプの定義
 3. 【次の一手 (Command)】：極小の具体的1アクション
"""

    def __init__(self, api_key: Optional[str] = None):
        key = api_key or DIRECT_API_KEY or os.environ.get("GEMINI_API_KEY")
        if not key:
            raise ValueError(f"GEMINI_API_KEY が設定されていません。探した場所: {env_path}")
        self.api_key = key

        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-3.7-flash"  # ★ 指定の gemini-3.7-flash で固定

        # 軽量マスターデータ
        self.stars = {
            "111": (6, "理想"), "011": (7, "リラックス"), "101": (9, "見栄"),
            "001": (3, "電気"), "110": (4, "平和主義"), "010": (1, "システム"),
            "100": (8, "経験値"), "000": (2, "才能")
        }

        # 設定キャッシュ（ゼロ遅延・低負荷）
        self._cached_config = types.GenerateContentConfig(
            system_instruction=self.SYSTEM_INSTRUCTION.strip(),
            temperature=0.7,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        )

        # ★ 会話セッションの初期化（これで会話が続きます）
        self.chat = self.client.chats.create(
            model=self.model_name,
            config=self._cached_config
        )

    def reset_conversation(self):
        """会話の文脈をリセットして初期状態に戻す"""
        self.chat = self.client.chats.create(
            model=self.model_name,
            config=self._cached_config
        )

    def _fast_scan(self, text: str) -> str:
        """軽量バイナリスキャン（最小限のメタ情報抽出）"""
        b1 = "1" if any(w in text for w in ["理想", "未来", "ビジョン", "平和", "全体", "仕組み"]) else "0"
        b2 = "1" if any(w in text for w in ["見せる", "広げる", "認め", "外", "人間関係", "評価"]) else "0"
        b3 = "1" if any(w in text for w in ["焦り", "急に", "トラブル", "動く", "走る", "一気に"]) else "0"
        bit = f"{b1}{b2}{b3}"

        star_num, star_name = self.stars.get(bit, (5, "宇宙"))
        color = "赤" if b3 == "1" and b2 == "1" else ("黒" if b3 == "0" and b1 == "0" else "青")
        return f"[Status:{color}|Code:{star_num}:{star_name}]"

    def interact(self, user_input: str) -> str:
        """会話を継続しながら応答を生成"""
        cmd_match = re.match(r"^/(scan|upgrade|othello|geek|chiikawa|future)\s*(.*)", user_input.strip())
        cmd, raw_text = (cmd_match.group(1), cmd_match.group(2)) if cmd_match else ("auto", user_input)

        # 軽量メタタグを付与
        meta_tag = self._fast_scan(raw_text)
        final_prompt = f"{meta_tag} [Cmd:{cmd}]\n{raw_text}"

        # ★ 会話履歴を保持したままメッセージ送信
        response = self.chat.send_message(message=final_prompt)
        return response.text


# ==============================================================================
# 実行エントリーポイント（連続会話テスト）
# ==============================================================================
if __name__ == "__main__":
    sakura = SakuraGeminiEngine()
   
    print("=== 桜🌸Geminiとの対話スタート（'exit'で終了） ===")
   
    # 連続会話シミュレーション
    test_conversations = [
        "さくらちゃん、今日ちょっと疲れちゃったな〜",
        "でも明日までに企画書出さなきゃいけなくて、なんか焦るんだよね。",
        "/chiikawa どうすればいい！？",
        "ありがとう！ちょっとお茶飲んで落ち着いたよ。"
    ]

    for user_msg in test_conversations:
        print(f"\nあなた: {user_msg}")
        reply = sakura.interact(user_msg)
        print(f"さくら🌸:\n{reply}")
