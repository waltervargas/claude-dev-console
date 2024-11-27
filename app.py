import streamlit as st
import anthropic
import base64
import re

# Define different template types
TEMPLATE_TYPES = {
    "generate": {
        "system_prompt": """You are an expert C programmer specialized in code generation and optimization. 
When providing code solutions:
1. Always include necessary header files
2. Follow C best practices and standards
3. Add comprehensive comments
4. Consider memory management carefully
5. Include error handling where appropriate
6. Provide example usage""",

        "template": """Generate C code for the following task:

REQUIREMENTS:
{requirements}

CONSTRAINTS:
{constraints}

First, if provided, review the existing code:
<current_code>
{code}
</current_code>

Please provide:
1. Complete implementation with proper error handling
2. Detailed explanation of the implementation
3. Memory management details
"""
    },

    "segfault": {
        "system_prompt": """You are an expert C debugger specialized in memory-related issues and segmentation faults. 
When analyzing code:
1. Check for common causes of segfaults
2. Analyze pointer usage and memory access
3. Look for array bounds violations
4. Verify memory allocation/deallocation
5. Check for null pointer dereferences""",

        "template": """Analyze this C code for potential segmentation faults:

CODE:
<current_code>
{code}
</current_code>

OBSERVED BEHAVIOR:
{behavior}

Please provide:
1. Identification of potential segfault causes
2. Line-by-line analysis of dangerous memory operations
3. Fixed version of the code
4. Recommendations to prevent similar issues
5. Suggested debugging steps with GDB"""
    }
}

def main():
    client = anthropic.Anthropic()

    st.set_page_config(page_title="C Code Assistant", layout="wide")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar for input
    with st.sidebar:
        st.header("C Code Assistant")

        # Template selection
        template_type = st.selectbox(
            "Select Task Type",
            ["Generate Code", "Analyze Segfault"]
        )


        # Input for base64 encoded code
        encoded_code = st.text_area(
            "Enter base64 encoded C code (within <code> tags)",
            height=150,
            placeholder="<code>base64_encoded_content</code>"
        )

        if template_type == "Generate Code":
            requirements = st.text_area(
                "Requirements",
                height=100,
                placeholder="Describe what the code should do..."
            )

            constraints = st.text_area(
                "Constraints",
                height=100,
                placeholder="Specify any constraints (performance, memory, etc.)"
            )

            if st.button("Generate Code"):
                template_key = "generate"
                prompt = TEMPLATE_TYPES[template_key]["template"].format(
                    requirements=requirements,
                    constraints=constraints,
                    code=encoded_code if encoded_code else "No reference code provided"
                )
                st.session_state.messages.append({"role": "user", "content": prompt})

        elif template_type == "Analyze Segfault":
            behavior = st.text_area(
                "Describe the Segfault Behavior",
                height=100,
                placeholder="Describe when and how the segfault occurs..."
            )

            if st.button("Analyze Segfault"):
                template_key = "segfault"
                prompt = TEMPLATE_TYPES[template_key]["template"].format(
                    decoded_code=decode_base64_code(encoded_code),
                    behavior=behavior
                )
                st.session_state.messages.append({"role": "user", "content": prompt})

    # Main content area
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Generate response if there's a new prompt
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        template_key = "generate" if template_type == "Generate Code" else "segfault"

        with st.chat_message("assistant"):
            with client.messages.stream(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                temperature=0,
                system=TEMPLATE_TYPES[template_key]["system_prompt"],
                messages=[
                    *[{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages]
                ]
            ) as stream:
                response = st.write_stream(stream.text_stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Export options
    if st.session_state.messages:
        st.sidebar.divider()
        if st.sidebar.button("Export Generated Code"):
            last_response = st.session_state.messages[-1]["content"]
            st.sidebar.download_button(
                label="Download C File",
                data=last_response,
                file_name="generated_code.c",
                mime="text/plain"
            )

    # Chat input field at the bottom
    if prompt := st.chat_input("Ask follow-up questions or request modifications..."):
        # Add user's follow-up message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response using the current template context
        template_key = "generate" if template_type == "Generate Code" else "segfault"
        
        # Display assistant response
        with st.chat_message("assistant"):
            with client.messages.stream(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                temperature=0,
                system=TEMPLATE_TYPES[template_key]["system_prompt"] + """
                    This is a follow-up question in an ongoing conversation about C programming.
                    Maintain context from the previous messages and provide relevant assistance.""",
                messages=[
                    *[{"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages]
                ]
            ) as stream:
                response = st.write_stream(stream.text_stream)
        
        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Clear chat button
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

if __name__ == "__main__":
    main()