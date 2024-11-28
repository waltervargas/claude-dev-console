import streamlit as st
import anthropic

def st_session_init():
    # TODO: move to dao
    state_vals = {
        "messages": [],
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.7,
        "max_tokens": 150,
        "system_prompt": "You are a helpful assistant.",
        "top_k": 50,
        "top_p": 0.9,
    }
   
    for key, val in state_vals.items():
        if key not in st.session_state:
            st.session_state[key] = val

def main():

    client = anthropic.Anthropic()

    models = [
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307",
    ]

    st_session_init()

    st.set_page_config(
        page_title="Chat",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    with st.sidebar:
        st.header("Chat with the Assistant")
        st.session_state.temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=st.session_state.temperature, step=0.05)
        st.session_state.max_tokens = st.number_input("Max Tokens", min_value=50, max_value=8192, value=st.session_state.max_tokens, step=64)
        st.session_state.model = st.selectbox("Model", options=models)
        st.session_state.system_prompt = st.text_area("System Prompt", value="You are a helpful assistant.", height=100)
        st.session_state.top_k = st.number_input("Top K", min_value=0, max_value=100, value=7, step=1)
        st.session_state.top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.9, step=0.05)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type a message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with client.messages.stream(
                model=st.session_state["model"],
                max_tokens=st.session_state.max_tokens,
                temperature=st.session_state.temperature,
                system=st.session_state.system_prompt,
                messages=[
                    *[{"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages]
                ]
            ) as stream:
                response = st.write_stream(stream.text_stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    if st.sidebar.button("Clear Chat Memory"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()