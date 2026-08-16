from google import genai
import streamlit as st

# 【システム管理者ノート】サーバー通信の競合を防ぐため、新SDK標準のClientオブジェクトに一本化
client = genai.Client(api_key="ここにAPIキー")

st.title("父への手紙・メッセージ生成プロトコル")

# ユーザー入力（父に伝えたい要件や、今の気持ちなど）
user_input = st.text_input(
    "お父さんに伝えたいこと、または状況を入力してください:"
)

if user_input:
  # プロンプトの構築：父宛ての適切なトーンに自動補正するメタ指示を付与
  prompt = f"以下の内容を元にして、父親にあてた丁寧で温かみのある手紙・メッセージ文面を作成してください。\n\n内容: {user_input}"

  with st.spinner("量子演算中... 文面を生成しています"):
    # 最新の gemini-2.5-flash または指定モデルで実行
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    st.write("### 生成されたメッセージ文面")
    st.write(response.text)
