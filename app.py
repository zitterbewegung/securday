from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os, time, yaml
from collections import deque
from typing import Dict, List, Optional, Any
# from agent import BabyAG
from langchain import Wikipedia, OpenAI
from langchain.llms import PromptLayerOpenAI
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from langchain.agents import Tool, AgentType
from langchain.chains import SimpleSequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferMemory
from langchain import PromptTemplate, LLMChain
from langchain.utilities import SerpAPIWrapper
from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from langchain.agents import load_tools, initialize_agent
from langchain.agents.react.base import DocstoreExplorer
from langchain.agents.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain.agents import Tool, AgentExecutor
from langchain.tools.python.tool import PythonREPLTool
from langchain.tools.ifttt import IFTTTWebhook
from langchain.utilities import WikipediaAPIWrapper, PythonREPL, BashProcess, TextRequestsWrapper
from transformers import AutoTokenizer, AutoModelForCausalLM
from shodan import Shodan
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain.chat_models import ChatOpenAI
from pwn import *
app = Flask(__name__)
memory = ConversationBufferMemory()
wolfram = WolframAlphaAPIWrapper()
wikipedia = WikipediaAPIWrapper()
python_repl = PythonREPLTool()
search = SerpAPIWrapper()
bash  = BashProcess()
requests = TextRequestsWrapper()

#model_name = "databricks/dolly-v1-6b"
#dolly_tokenizer = AutoTokenizer.from_pretrained(model_name)
#dolly_model = AutoModelForCausalLM.from_pretrained(model_name).to("cuda")

#model_name = "PygmalionAI/pygmalion-2.7b"
#tokenizer = AutoTokenizer.from_pretrained(model_name)
#model = AutoModelForCausalLM.from_pretrained(model_name)

def subset_shodan(ip: str):
    api = Shodan(os.environ.get('SHODAN_API_KEY'))
    host = api.host(ip)
    return """
    IP: {}
    Organization: {}
    Operating System: {}
    Location: Lat {} Long {}
    Asn: {}
    Transport: {}
    """.format(host['ip_str'],
               host.get('org', 'n/a'),
               host.get('os', 'n/a'),
               host.get('lat', 'n/a'),
               host.get('long', 'n/a'),
               host.get('asn', 'n/a'),
               host.get('transport', 'n/a'))


 
def pygmalion_run(message):

    inputs  = tokenizer(message, return_tensors="pt")
    result  = model.generate(**inputs)
    content =  tokenizer.decode(result[0])
    content = content.replace("\\r\\n", "")
    return content

def dolly_run(message):

    inputs = tokenizer(message, return_tensors="pt")
    result = model.generate(**inputs)
    return tokenizer.decode(result[0])
     


tools = [
    Tool(name='pygmalion',
         func=pygmalion_run,
         description='useful when you are replying to romantic conversation.'),
    
    Tool(name='shodan', 
         func=subset_shodan,
         description='useful when you need to search shodan.',
    ),
    Tool(
        name="wolfram",
        func=wolfram.run,
        description="useful for calculations and mathematical quesions.",
    ),
    Tool(
        name="python_repl",
        func=python_repl.run,
        description="use this when asked about writing code or if py in is the request.",
    ),
    Tool(
        name="wikipedia",
        func=wikipedia.run,
        description="use this when looking for historical or general questions.",
    ),
    Tool(
        name="Search",
        func=search.run,
        description="useful general questions but not shodan.",
    ),
    Tool(
        name="Bash",
        func=bash.run,
        description="use this to execute shell commands or git commits",
        ),
    Tool(
        name="Google Places",
        func=bash.run,
        description="use this to get information about a place, restaurant or hotel..",
        ),
    
]


#llm_female_refined_llama = LlamaCpp(model_path="./ggml-model-q4_0.bin")
#llm_female_refined_chain_llama = LLMChain(prompt=prompt, llm=llm)

#template = """Question: {question} Answers think step by step."""
#prompt = PromptTemplate(template=template, input_variables=["question"])

prefix = """The following is a conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. The AI can write code and execute it. If the AI doesn't know the answer to a question, it truthfully says it does not know. You have access to the following tools: """
suffix = (
    "Begin!\n\nPrevious conversation history:\n{chat_history}\n\nNew input: {input}\n{agent_scratchpad}"
    ""
)

message_history = RedisChatMessageHistory(
    url="redis://localhost:6379/0", ttl=600, session_id="my-session"
)

memory = ConversationBufferMemory(
    memory_key="chat_history", chat_memory=message_history
)

agent_chain = initialize_agent(
    tools,
    llm=ChatOpenAI(temperature=0.0),
    #llm=OpenAI(model='gpt-3.5-turbo', temperature=(0.0)),
    #agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    agent= AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
    max_iterations=5,
    early_stopping_method="generate",
    max_execution_time=15,
    #max_iterations=1,
)

def split_string(input_string, max_length=320):
    strings_list = []
    input_string_length = len(input_string)

    for i in range(0, input_string_length, max_length):
        strings_list.append(input_string[i:i + max_length])

    return strings_list

@app.route("/sms", methods=["POST"])
def chatgpt():
    """get incoming message"""
    inb_msg           = request.form["Body"]  # .lower()
    print(inb_msg)


    response = agent_chain.run(input=inb_msg)

    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    # time.sleep(2)
    resp = MessagingResponse()
    # Add a message
    for msg in split_string(response):
        resp.message(msg)
    print(response)

    return str(resp)


if __name__ == "__main__":
    
    app.run(debug=True)
