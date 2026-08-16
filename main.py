import streamlit as st
import google.generativeai as genai

# サーバーが混乱しないよう「genai」に一本化した設定
genai.configure(api_key="ここにAPIキー")

model = genai.GenerativeModel("gemini-3.7-flash")

user_input = st.text_input("入力:")

if user_input:
    response = model.generate_content(user_input)
    st.write(response.text)
