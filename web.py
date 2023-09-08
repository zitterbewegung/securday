import streamlit as st
from inference import agent_chain

st.header('Tagline Generation App')
st.text('(Powered by GPT-3 Model)')


prompt = st.text_area('Enter your prompt', "", height=5)
trigger = st.button("Generate")
st.subheader("Result")

if trigger:
    #response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=temp, max_tokens=mt)             result = agent_chain.run(input=body)

    result = agent_chain.run(input=prompt)
    st.write(result)
