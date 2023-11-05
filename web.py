import streamlit as st
from inference import agent_chain

st.header("Saturday: A natural language network scanner.")
gh_url = 'https://github.com/zitterbewegung/saturday'
st.text("(Powered by langchain, shodan and Python!)")
st.write("the code is at [link](%s)" % gh_url)
prompt = st.text_area("Enter your prompt", "", height=5)
trigger = st.button("Scan")
st.subheader("Result")

if trigger:
    # response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=temp, max_tokens=mt)             result = agent_chain.run(input=body)

    result = agent_chain.run(input=prompt)
    st.write(result)
