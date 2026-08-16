import os
import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. ページ基本設定
# ==========================================
st.set_page_config(
    page_title="Gemini 3.7 Flash API",
    page_icon="🌸",
    layout="centered"
)

# ==========================================
# 2. APIキーの設定（環境変数またはSecretsから安全に取得）
# ==========================================
# ※ Streamlit Cloudの場合は st.secrets["GEMINI_API_KEY"]
# ※ ローカルの場合は os.environ.get("GEMINI_API_KEY") または直接代入
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY", "")

if not api_key:
    st.error("🚨 APIキーが設定されていません。.streamlit/secrets.toml または環境変数を確認してください。")
    st.stop()

genai.configure(api_key=api_key)

# ==========================================
# 3. モデル初期化（Gemini 3.7 Flash）
# ==========================================
model = genai.GenerativeModel("gemini-3.7-flash")

# ==========================================
# 4. UI構築
# ==========================================
st.title("🌸 Gemini 3.7 Flash API 接続テスト")
st.caption("Python 3.14 環境対応クリーンコード")

user_input = st.text_input("メッセージを入力してください：")

if st.button("送信") and user_input:
    with st.spinner("思考中..."):
        try:
            response = model.generate_content(user_input)
            st.markdown("### 応答結果")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
