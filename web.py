import streamlit as st
from inference import agent_chain

st.header("Saturday: A natural language network scanner.")
gh_url = 'https://github.com/zitterbewegung/saturday'
st.text("(Powered by langchain, shodan and Python!)")
st.write("the code is at [link](%s)" % gh_url)
st.header("Securday: Natural Language Network Scanner")
st.text("(Powered by GPT-3 Model)")
st.text("Try: Does defcon.org use HTTP/2?")
st.text("Or what ports are open on 1.1.1.1?")

prompt = st.text_area("Enter your prompt", "", height=5)
trigger = st.button("Scan")
st.subheader("Result")

if trigger:
    # response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=temp, max_tokens=mt)             result = agent_chain.run(input=body)

    result = agent_chain.run(input=prompt)
    st.write(result)
