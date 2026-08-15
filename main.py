import os
import time
from google import genai
from google.genai import types
import streamlit as st

# setup_sakura.py から設定と演算エンジンを読み込み
from setup_sakura import LocalCosmicEngine, SAKURA_CORE_PROMPT

# ==============================================================================
# 0. ページ設定 & クライアント初期化
# ==============================================================================
ICON_IMAGE = "Gemini_Generated_Image_hqicthqicthqicth.png"

st.set_page_config(
    page_title="桜🌸Gemini",
    page_icon=ICON_IMAGE,
    layout="centered"
)

# APIキー取得 & クライアント初期化
API_KEY = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
client = genai.Client(api_key=API_KEY)
MODEL_ID = "gemini-3.7-flash"

cosmic_engine = LocalCosmicEngine()

# ==============================================================================
# 1. セッション管理 & 即答チューニング（503回避）
# ==============================================================================
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model=MODEL_ID,
        config=types.GenerateContentConfig(
            system_instruction=SAKURA_CORE_PROMPT,
            temperature=0.7,
            thinking_config=types.ThinkingConfig(thinking_budget=1024),  # 即答化
        )
    )

if "messages" not in st.session_state:
    st.session_state.messages = []
    # 初回アクセス（宇宙接続）
    try:
        init_res = st.session_state.chat.send_message("ここは宇宙です")
        st.session_state.messages.append({"role": "assistant", "content": init_res.text})
    except Exception:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "桜ジェミニの桜だよ。リンリンリン宇宙の鈴を鳴らして待ってたよ。今日も1日よろしくね🌸✨"
        })

# タイトル表示
st.title("🌸 桜 Gemini")
st.caption("宇宙剣士・桜（Gemini 3.7 Flash 稼働中）")

# 過去ログの描画（アイコン画像付き）
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar=ICON_IMAGE):
            st.markdown(msg["content"])

# ==============================================================================
# 2. 対話ハンドリング & 自動リトライ
# ==============================================================================
user_input = st.chat_input("メッセージを入力... (終了時は「ここは地球です」)")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 宇宙演算メトリクス算出
    metrics = cosmic_engine.evaluate(user_input)
    augmented_prompt = (
        f"[内部宇宙演算データ: 九星={metrics['star_label']} | "
        f"十二支={metrics['zodiac']}({metrics['phase']}) | "
        f"ゆらぎ度={metrics['intensity']:.1f}/100]\n"
        f"ユーザー入力: {user_input}"
    )

    with st.chat_message("assistant", avatar=ICON_IMAGE):
        message_placeholder = st.empty()
        response_text = ""
        
        # 503エラー時の一時回避リトライ（最大3回）
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = st.session_state.chat.send_message(augmented_prompt)
                response_text = response.text
                break
            except Exception as e:
                if ("503" in str(e) or "UNAVAILABLE" in str(e)) and attempt < max_retries - 1:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                response_text = f"宇宙の通信波にノイズが入ったみたい🌸（エラー: {e}）"
                break
        
        message_placeholder.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
