import streamlit as st

def get_prompt_input():
    prompt = st.text_area("Enter your prompt", placeholder="<Enter your prompt here>")
    return prompt

def get_existing_code():
    code = st.text_area("CODE in base64", placeholder="")
    return code

def get_additional_file_input():
    additional_file = st.file_uploader("Upload additional files", type=[
        "py", "txt", "json", "x-xpixmap", "xpm"])
    return additional_file