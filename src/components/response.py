import streamlit as st
from src.services.claude import call_claude_sonnet_3_5

def display_response_markdown(system, assistant, prompt, code, additional_file):
    if st.button("Run"):
        prompt = prompt.replace("{{EXISTING_CODE}}", code)
        prompt = prompt.replace("{{ADDITIONAL_FILE}}", additional_file)
        response = call_claude_sonnet_3_5(system, prompt, assistant)
        st.markdown(response)