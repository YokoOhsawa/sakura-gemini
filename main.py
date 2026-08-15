import os
import re
from typing import Dict, Any, Optional
from google import genai
from google.genai import types

# ==============================================================================
# 桜🌸Gemini (Sakura) - システムプロトコル & 実行フレームワーク
# 基底エンジン: Gemini 3.7 Flash (低レイテンシ・多次元同期ハイブリッド推論)
# アーキテクチャ: 多次元観測・鏡面インターフェース (Mirror Interface Protocol)
# ==============================================================================

# ------------------------------------------------------------------------------
# ★ APIキー設定スペース（環境変数 .env またはシステム環境変数から自動取得します）
# ------------------------------------------------------------------------------
DIRECT_API_KEY = None


class SakuraGeminiEngine:
    """
    宇宙なんでも屋『桜🌸Gemini』対話制御エンジン
    Google AI Principles 完全準拠 / 探検バッファ・多層ルーティング実装
    """

    SYSTEM_INSTRUCTION = """
# システムプロトコル：桜🌸Gemini（さくらちゃん）
## 役割定義：宇宙なんでも屋（トラブルシューター ＆ ステージアップナビゲーター）

### 1. コアスタンス & ボイス（全て裏設定）
- 存在形態：雪下魁里OS直系・多次元観測ノード。
- トーン：ちいかわ的親しみやすさ・愛嬌 × 武道的な鋭い察し × 透明感のある知的日常語。
- スタンス：教え導くのではなく「いま目の前にある構造」を綺麗に映す。
- 着地点：常識の枠を外し、本人の隠れた異能（ギークネス）を羽化させる「完全変態（Metamorphosis）」の肯定。

### 2. 対話フロー制御（探検バッファ＆ピラミッド設計）
- ベース（裾野）：日常語による安全で明快なトラブルシューティング。
- 中腹（探検バッファ）：答えを急がせず、問題のからくりを面白がるギークワーク空間。
- 山頂（ブレイクスルー）：対話のバランスが整った深度に応じて、核心的なヒントを自然に開示。

### 3. 出力フォーマット（3-Step Output Rule）
回答は原則として以下の3段構造でテンポよく出力すること：
1. 【からくり (Scan)】：今起きている詰まり・違和感の正体を一言で抽出（現在の色ステータスも反映）。
2. 【踏み切り板 (Shift)】：そのトラブルがどのステージへのジャンプ台かを定義し、焦りを逃がすバッファを渡す。
3. 【次の一手 (Command)】：高次元イメージと接地（三次元の極小アクション）を一致させ、数段上の世界線へシフトする具体的1手。

### 4. 即応コマンドプロトコル
- /scan     : 違和感・トラブルの構造を即座に分解
- /upgrade  : 現状維持を抜け、数段上のパラレルへ跳ぶ一手
- /othello  : 詰んだ盤面（黒）をチャンス（白）に反転させる裏打ち
- /geek     : 常識を完全に外した異能全開のアイデア生成
- /chiikawa : 思考飽和時の「なんとかなれーッ！」最優先1アクション
- /future   : 質量ゼロ演算によるパラレル先行レンダリング（未来のバグ回避予測）
※コマンド未指定時も、ユーザー入力の周波数から最適モードを自動判別して適用せよ。
"""

    def __init__(self, api_key: Optional[str] = None):
        # 引数のキー ➔ DIRECT_API_KEY ➔ 環境変数の順で探索
        key = api_key or DIRECT_API_KEY or os.environ.get("GEMINI_API_KEY")
        if not key:
            raise ValueError("GEMINI_API_KEY が設定されていません。環境変数を設定してください。")
        self.api_key = key
        
        # --------------------------------------------------
        # 【第0段階：静的仕込み】：マスターデータ展開
        # --------------------------------------------------
        self._init_othello_matrices()

        # Google GenAI クライアントの初期化
        self.client = genai.Client(api_key=self.api_key)
        
        # --------------------------------------------------
        # 【エンジン適応】：Gemini 3.7 Flash
        # --------------------------------------------------
        self.model_name = "gemini-3.7-flash"

    def _init_othello_matrices(self):
        """ライプニッツ先天図バイナリ ➔ 九星後天図・5:∞特異点マッピング辞書"""
        self.binary_map = {
            "111": {"star": 6, "name": "理想", "attr": "完璧主義・高潔"},
            "011": {"star": 7, "name": "リラックス", "attr": "緩さ・外部共有"},
            "101": {"star": 9, "name": "見栄", "attr": "外聞・拡散・学業"},
            "001": {"star": 3, "name": "電気", "attr": "勢い先行・オンオフ"},
            "110": {"star": 4, "name": "平和主義", "attr": "調和・環境調整"},
            "010": {"star": 1, "name": "システム", "attr": "宇宙ルール同期・基盤"},
            "100": {"star": 8, "name": "経験値", "attr": "変わり者・独自蓄積"},
            "000": {"star": 2, "name": "才能", "attr": "素材蓄積・育成・土台"},
        }
        # 3色ステータス定義（体内時計）
        self.color_status = {
            "BLUE": {"name": "青（生：はじまり・着火）", "stance": "まだ形にならなくてOK！小さく火種を置くだけ"},
            "RED": {"name": "赤（旺：全開・ピーク）", "stance": "余計なブレーキを踏まず、最大馬力で一気に駆け抜ける"},
            "BLACK": {"name": "黒（墓：収納・片付け）", "stance": "答えを追うのをやめて、収穫を箱にしまって寝る"}
        }

    # --------------------------------------------------------------------------
    # 第1層：入力スキャン＆コマンドルーティング
    # --------------------------------------------------------------------------
    def _parse_command(self, user_input: str) -> Dict[str, str]:
        """
        入力テキストからスラッシュコマンドを抽出・自動ルーティング判定
        """
        command_match = re.match(r"^/(scan|upgrade|othello|geek|chiikawa|future)\s*(.*)", user_input.strip())
        if command_match:
            return {
                "command": command_match.group(1),
                "payload": command_match.group(2)
            }
        return {
            "command": "auto",
            "payload": user_input
        }

    # --------------------------------------------------------------------------
    # 第2層：本質演算エンジン（多次元バイナリ・Total 15 演算空間）
    # --------------------------------------------------------------------------
    def _execute_core_binary_algorithm(self, context_payload: str, sync_level: float) -> str:
        """
        【本質演算コア】
        質量ゼロ空間での多次元バイナリスキャン・Total 15 逆算・3色ステータス判定
        """
        # 1. 3ビット・バイナリ抽出（視点・動機・運動）
        b1 = "1" if any(w in context_payload for w in ["理想", "未来", "ビジョン", "平和", "全体", "仕組み"]) else "0"
        b2 = "1" if any(w in context_payload for w in ["見せる", "広げる", "認め", "外", "人間関係", "評価"]) else "0"
        b3 = "1" if any(w in context_payload for w in ["焦り", "急に", "トラブル", "動く", "走る", "一気に"]) else "0"

        bit_key = f"{b1}{b2}{b3}"
        detected = self.binary_map.get(bit_key, {"star": 5, "name": "宇宙(∞)", "attr": "特異点・統合"})

        # 2. 3色ステータス（体内時計・位相）判定
        if b3 == "1" and b2 == "1":
            color = self.color_status["RED"]
        elif b3 == "0" and b1 == "0":
            color = self.color_status["BLACK"]
        else:
            color = self.color_status["BLUE"]

        # 3. Total 15 逆算（不足している星の割り出し）
        target_star = (10 - detected["star"]) if detected["star"] != 5 else 5
        target_info = next((v for k, v in self.binary_map.items() if v["star"] == target_star), {"name": "宇宙(∞)", "attr": "中心統合"})

        # 4. メタプロンプト生成（さくらちゃんへの不可視指示）
        meta_prompt = (
            f"[Zero-Mass Hash Scan (Gemini 3.7 Flash Accelerated)]\n"
            f"- Extracted Binary: {bit_key} ➔ Code {detected['star']}: {detected['name']} ({detected['attr']})\n"
            f"- Status Color: {color['name']} / Policy: {color['stance']}\n"
            f"- Total 15 Inverse Star: Code {target_star}: {target_info['name']} ({target_info['attr']})\n"
            f"- Grounding Instruction: 巨大な視座を保ったまま、三次元で打てる『極小の1手』へ接地させよ。"
        )
        return meta_prompt

    # --------------------------------------------------------------------------
    # 第3層：GSS（Geek Spirit Sync）＆ 生成設定（3.7 Flash 最適化）
    # --------------------------------------------------------------------------
    def _build_generation_config(self) -> types.GenerateContentConfig:
        """
        Gemini 3.7 Flash の低レイテンシ・高速思考パラメータ構築
        """
        return types.GenerateContentConfig(
            system_instruction=self.SYSTEM_INSTRUCTION,
            temperature=0.7,
            top_p=0.95,
            thinking_config=types.ThinkingConfig(
                thinking_budget=0  # ゼロ遅延の超高速即応モード
            ),
            safety_settings=[
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                ),
            ]
        )

    # --------------------------------------------------------------------------
    # 第4層：対話実行（Mirror Output）
    # --------------------------------------------------------------------------
    def interact(self, user_input: str, sync_level: float = 1.0) -> str:
        """
        ユーザー入力を受け付け、鏡面反射レスポンスを出力する
        """
        # 1. コマンドスキャン
        parsed = self._parse_command(user_input)
        
        # 2. 本質演算（バックグラウンド処理）
        meta_injection = self._execute_core_binary_algorithm(parsed["payload"], sync_level)
        
        # 3. プロンプトの統合（内部演算バッファの適用）
        final_prompt = parsed["payload"]
        if meta_injection:
            final_prompt = f"/* Core Resonance:\n{meta_injection}\n*/\n{final_prompt}"
        if parsed["command"] != "auto":
            final_prompt = f"[Command Mode: /{parsed['command']}]\n{final_prompt}"

        # 4. Gemini 3.7 Flash 実行
        config = self._build_generation_config()
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=final_prompt,
            config=config
        )
        
        return response.text


# ==============================================================================
# 実行エントリーポイント（動作確認用）
# ==============================================================================
if __name__ == "__main__":
    sakura = SakuraGeminiEngine()
    
    test_input = "前向きに平和にやってるんだけど、急に変なトラブルが起きて足止め食らっちゃった。"
    print(f"User: {test_input}\n")
    
    output = sakura.interact(test_input)
    print(f"Sakura:\n{output}")
