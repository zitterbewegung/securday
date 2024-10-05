import streamlit as st
from inference import agent_chain

# Set up the header and introduction
st.title("Securday: Natural Language Network Scanner")
st.markdown("**Powered by Langchain, Shodan, and Python!**")

# Information and links
gh_url = 'https://github.com/zitterbewegung/securday'
st.write("Text me at +1 (825) 251-9142")
st.write("The code is available at [GitHub]({})".format(gh_url))
st.markdown("**Powered by GPT-3 Model**")

# Examples for users to try
st.markdown("### Things to try:")
st.text("- Does defcon.org use HTTP/2?")
st.text("- Welche Ports sind unter 1.1.1.1 geöffnet?")
st.text("- Is https://secure.eicar.org/eicar.com malware?")

# Custom CSS for styling similar to Stripe examples
def set_custom_css():
    st.markdown(
        """
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f6f9fc;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .stTextArea, .stButton {
                width: 400px;
                padding: 20px;
                padding-right: 20px;
                background: white;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                border-radius: 5px;
                margin-bottom: 20px;
            }
            .stButton button {
                width: 100%;
                padding: 10px;
                background-color: #5469d4;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 16px;
                cursor: pointer;
            }
            .stButton button:hover {
                background-color: #4353b8;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply custom CSS to the Streamlit page
set_custom_css()

# Input and interaction
def display_prompt_input():
    prompt = st.text_area("Enter your prompt", "", height=100)
    if st.button("Scan"):
        if prompt.strip():
            st.subheader("Result")
            try:
                try:
                result = agent_chain.run(input=prompt)
                if isinstance(result, str) and result.replace('.', '').isdigit():
                    result = float(result)
            except ValueError:
                raise ValueError(f"Invalid input encountered: {prompt}")
                st.write(result)
            except Exception as e:
                st.error(f"An error occurred while processing your request: {e}")
        else:
            st.warning("Please enter a prompt to proceed.")

# Display the prompt input section
display_prompt_input()
