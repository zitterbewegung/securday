import streamlit as st
from inference import agent_chain

st.header("Securday: Natural Language Network Scanner")
gh_url = 'https://github.com/zitterbewegung/securday'
st.text("(Powered by langchain, shodan and Python!)")
st.text("Text me at +1 (825) 251-9142")
st.write("the code is at [link](%s)" % gh_url)
st.text("(Powered by GPT-3 Model)")
st.text("Things to try: Does defcon.org use HTTP/2?")
st.text("Welche Ports sind unter 1.1.1.1 geöffnet?")
st.text("Is https://secure.eicar.org/eicar.com malware?")

prompt = st.text_area("Enter your prompt", "", height=5)
trigger = st.button("Scan")
st.subheader("Result")

if trigger:
    # response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=temp, max_tokens=mt)             result = agent_chain.run(input=body)

    result = agent_chain.run(input=prompt)
    st.write(result)
