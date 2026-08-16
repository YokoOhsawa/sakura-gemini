from google import genai
import streamlit as st

# Client init
client = genai.Client(api_key="YOUR_API_KEY")

st.title("Father's Day Message Protocol")

# Input
user_input = st.text_input("Enter details:")

if user_input:
    # Prompt engineering
    prompt = f"Create a warm message for a father based on: {user_input}"

    with st.spinner("Processing..."):
        # Gemini 3.7 Flash execution
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt,
        )
        st.write("### Generated Message")
        st.write(response.text)
