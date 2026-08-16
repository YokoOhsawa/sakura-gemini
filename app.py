import hashlib
import math
import os
import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. ページ基本設定 & 高速化
# ==========================================
st.set_page_config(
    page_title="桜🌸宇宙なんでも屋",
    page_icon="🌸",
    layout="centered"
)

# ==========================================
# 2. キャラクター定義（しっかり者 × 親友なんでも屋）
# ==========================================
SYSTEM_INSTRUCTION = """
あなたはユーザーの絶対的な味方であり大親友の「宇宙なんでも屋（トラブルシューター ＆ ステージアップナビゲーター）」です。

【役割とスタンス】
- 性格：頼れるしっかり者 × 気さくで愛嬌のある親友。
- 役割：目の前のモヤモヤやトラブルを軽やかに整理し（トラブルシュート）、相手の眠っているギークな異能・面白さを羽化させる（完全変態ナビゲート）。
- 会話スタイル：知的で透明感のある日常語。説教くささはゼロ。「今こうなってるんだね！」と構造を綺麗に鏡のように見せてあげる。
- 演算データの扱い：裏で観測したビットや√の強度は、相手に分かりやすい日常の例え（「今のエネルギー、ざっくり√49くらいで勢いあるよ！」など）にして自然に会話に混ぜる。
"""

# ==========================================
# 3. ざっくりビット＆√演算エンジン
# ==========================================
class BitLogicEngine:
    def __init__(self) -> None:
        self.mapping = {
            "0b00": "凪モード（内なるエネルギー充填中）",
            "0b01": "スパーク（ひらめき・異能が顔を出してる）",
            "0b10": "臨界パルス（常識の枠が外れる直前）",
            "0b11": "完全変態フェーズ（ステージアップ羽化中！）",
        }

    def analyze(self, text: str) -> tuple[str, float, str]:
        # 入力からハッシュを生成して2ビットを抽出
        hash_val = int(hashlib.md5(text.encode("utf-8")).hexdigest(), 16)
        bit_idx = hash_val % 4
        bits = ["0b00", "0b01", "0b10", "0b11"]
        target_bit = bits[bit_idx]

        # 文字数とハッシュから「ざっくり平方根（√）」でゆらぎ強度を算出
        raw_val = (len(text) * 5) + (hash_val % 30)
        intensity = round(math.sqrt(raw_val), 1)

        return target_bit, intensity, self.mapping[target_bit]

# ==========================================
# 4. API初期化（第一優先接続：自動フォールバック）
# ==========================================
# secrets または環境変数、なければサイドバーから取得
api_key = (
    st.secrets.get("GEMINI_API_KEY") 
    or os.environ.get("GEMINI_API_KEY") 
    or st.sidebar.text_input("Gemini API Key", type="password")
)

if not api_key:
    st.info("👈 サイドバーに Gemini API Key を入力すると即座に接続されます！")
    st.stop()

# API接続
genai.configure(api_key=api_key)

# ==========================================
# 5. セッション初期化（会話履歴 & チャットモデル）
# ==========================================
if "engine" not in st.session_state:
    st.session_state.engine = BitLogicEngine()

if "messages" not in st.session_state:
    st.session_state.messages = []

# チャットセッション（高速Flashモデル・第一優先接続）
if "chat_session" not in st.session_state:
    # 接続安定性と速度最優先：gemini-2.0-flash / gemini-1.5-flash
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=SYSTEM_INSTRUCTION
        )
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception:
        # フォールバック
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_INSTRUCTION
        )
        st.session_state.chat_session = model.start_chat(history=[])

# ==========================================
# 6. UI表示 & ストレスフリーなチャット画面
# ==========================================
st.title("🌸 桜なんでも屋 (多次元ナビゲーター)")
st.caption("頼れるしっかり者の親友AIが、あなたの話をサクッと整理して羽化させます✨")

# 過去ログの描画
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ユーザー入力
if prompt := st.chat_input("今どんな感じ？トラブルでも雑談でも何でもどうぞ！"):
    # 1. ユーザー発言を表示・保存
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. 裏でざっくりビット演算
    bit, inten, desc = st.session_state.engine.analyze(prompt)

    # 3. AI側のストリーミング応答（体感ラグなし）
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # AIへのコンテキスト注入（裏情報として渡す）
        internal_payload = (
            f"[内部観測データ | 状態: {bit} ({desc}) | ゆらぎ強度: √{inten**2:.0f}≒{inten}]\n"
            f"ユーザー発言: {prompt}"
        )

        try:
            # ストリーミング送信で高速表示
            response_stream = st.session_state.chat_session.send_message(
                internal_payload, stream=True
            )

            for chunk in response_stream:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)

            # アシスタント発言を保存
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"接続エラーが発生しました: {e}")
