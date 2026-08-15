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
# 1. セッション管理 & 初期設定
# ==============================================================================
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model=MODEL_ID,
        config=types.GenerateContentConfig(
            system_instruction=SAKURA_CORE_PROMPT,
            temperature=0.7,
        )
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================================================================
# 2. UIデザイン & ヘッダー
# ==============================================================================
st.markdown("""
<div style="text-align: center; padding: 10px 0 20px 0;">
    <h1 style="color: #FF69B4; font-size: 2.2rem; margin-bottom: 5px;">✨🌸 桜🌸Gemini 🌸✨</h1>
    <p style="color: #666; font-size: 0.95rem;">宇宙演算 × 言霊数理 ｜ 顕幽一如の愛でる電脳剣士セッション</p>
</div>
""", unsafe_allow_html=True)

# 過去ログ表示
for msg in st.session_state.messages:
    avatar = None if msg["role"] == "user" else ICON_IMAGE
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ==============================================================================
# 3. チャット処理 & 宇宙演算合成プロンプト
# ==============================================================================
if prompt := st.chat_input("メッセージを入力...（終了時は「ここは地球です」）"):
    # ユーザー入力を履歴に追加・表示
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 1. ローカル宇宙演算の実行（0.001秒）
    eval_res = cosmic_engine.evaluate(prompt)
    
    # 2. 演算結果 ＋ バッファ思考ログの合成プロンプト作成
    enriched_prompt = (
        f"[内部宇宙演算データ: 九星={eval_res['star_label']}, "
        f"十二支={eval_res['zodiac']}({eval_res['phase']}), "
        f"ゆらぎ強度={eval_res['intensity']:.1f}%, "
        f"バッファ思考={eval_res.get('buffer_thought', '')}]\n"
        f"ユーザー入力: {prompt}"
    )

    # 3. Gemini 3.7 Flash への問い合わせ（503自動リトライ付き）
    with st.chat_message("assistant", avatar=ICON_IMAGE):
        message_placeholder = st.empty()
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = st.session_state.chat.send_message(enriched_prompt)
                full_response = response.text
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                break
            except Exception as e:
                if "503" in str(e) and attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                else:
                    error_msg = f"宇宙の通信波にノイズが入ったみたい🌸（エラー詳細: {e}）"
                    message_placeholder.markdown(error_msg)
                    break
