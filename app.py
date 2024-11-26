import streamlit as st
from src.components.prompt import (
    get_prompt_input,
    get_existing_code,
    get_additional_file_input,
)

from src.components.response import (
    display_response_markdown,
)

def main():
    st.set_page_config(page_title="Anthropic Developer Console", layout="wide")
    
    if "code" not in st.session_state:
        st.session_state.code = ""
    
    if "additional_file" not in st.session_state:
        st.session_state.additional_file = None
    
    if "prompt" not in st.session_state:
        st.session_state.prompt = ""

    if "response" not in st.session_state:
        st.session_state.response = ""
    
    response = "Hello, World!"
    st.session_state.code = get_existing_code()
    st.session_state.additional_file = get_additional_file_input()
    st.session_state.prompt = get_prompt_input()
    st.session_state.response = display_response_markdown(
        "You are a seasoned C developer expert on \"Ray Casting\" and minilibx libft and game development.",
        """---""",
        st.session_state.prompt, 
        st.session_state.code, 
        st.session_state.additional_file)
if __name__ == "__main__":
    main()