import streamlit as st
import requests
import json

def main():
    st.title("Workbench Console")

    st.subheader("Raw Request and Response")

    # Sidebar specific to this page (if any)
    with st.sidebar:
        st.header("Workbench Console Settings")

    # Inputs for tweaking parameters
    with st.expander("Configure Parameters"):
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.05)
        max_tokens = st.number_input("Max Tokens", min_value=50, max_value=2048, value=150, step=50)
        model_selection = st.selectbox("Model Selection", options=["gpt-3.5-turbo", "gpt-4"])
        system_prompt = st.text_area("System Prompt", value="You are a helpful assistant.", height=100)
        top_k = st.number_input("Top K", min_value=0, max_value=100, value=50, step=5)
        top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.9, step=0.05)

    # Input for raw request
    default_request = {
        "model": model_selection,
        "prompt": "Hello, how can I assist you today?",
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_k": top_k,
        "top_p": top_p,
        "system_prompt": system_prompt
    }

    raw_request = st.text_area("Raw Request (JSON)", height=200, value=json.dumps(default_request, indent=4))

    if st.button("Send Request"):
        try:
            request_data = json.loads(raw_request)
            st.info("Sending request to the API...")
            
            # Placeholder for actual API endpoint
            api_endpoint = "https://api.openai.com/v1/your-endpoint"  # Replace with actual endpoint
            
            # Placeholder for headers (e.g., Authorization)
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer YOUR_API_KEY"  # Replace with your actual API key
            }
            
            response = requests.post(api_endpoint, headers=headers, json=request_data)
            
            st.subheader("Raw Response")
            st.text(response.text)
            
            # Optionally, parse and display the response in a formatted way
            try:
                response_json = response.json()
                st.json(response_json)
            except json.JSONDecodeError:
                st.warning("Response is not in JSON format.")
        
        except json.JSONDecodeError:
            st.error("Invalid JSON in raw request.")

if __name__ == "__main__":
    main()