import streamlit as st
from src.services.claude import call_claude_sonnet_3_5

def display_response_markdown(system, assistant, prompt, code, additional_file):
    if st.button("Run"):   
        if code is not None:
            prompt = prompt.replace("{{EXISTING_CODE}}", code)
        
        if additional_file is not None:
            prompt = prompt.replace("{{ADDITIONAL_FILE}}", additional_file.getvalue().decode("utf-8"))
        
        response = call_claude_sonnet_3_5(system, prompt, assistant)
        content = ""
        for c in response.content:
            content += c.text + "\n"
        st.markdown(content)