from langchain import Wikipedia, OpenAI
from langchain.llms import PromptLayerOpenAI
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from langchain.agents import Tool, AgentType
from langchain.chains import SimpleSequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferMemory
from langchain import PromptTemplate, LLMChain
#from langchain.utilities import SerpAPIWrapper
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
#import pwnlib
from langchain.chat_models import ChatOpenAI
import cve_searchsploit as CS
import ipaddress, os

memory = ConversationBufferMemory()
wolfram = WolframAlphaAPIWrapper()
wikipedia = WikipediaAPIWrapper()
python_repl = PythonREPLTool()
#search = SerpAPIWrapper()
bash  = BashProcess()
requests = TextRequestsWrapper()
CS.update_db()
exploit_db = CS.update_db()                                                                     
                                                                                        # Custom tools        
def query_exploits(CVE : str) -> str:
    pass

def subset_shodan(addr: str):
    
    #ry:
    #   ip = ipaddress.ip_address(addr)
    #xcept ValueError:
    #   return 'Invalid ip address'
    #ry:
    shodan_api = Shodan(os.environ.get('SHODAN_API_KEY'))
    host = shodan_api.host(addr)
    #xcept Exception as e:
    #  return "Shodan has no info"
    ports = ""
    for i in host['data']:
        ports += "Port {} \n".format(i['port'])
    return """
    IP: {}
    Organization: {}
    Operating System: {}
    Location: Lat {} Long {}
    Asn: {}
    Transport: {}
    Port: {}
    """.format(host['ip_str'],
               host.get('org', 'n/a'),
               host.get('os', 'n/a'),
               host.get('lat', 'n/a'),
               host.get('long', 'n/a'),
               host.get('asn', 'n/a'),
               host.get('transport', 'n/a'),
               ports,)

def scan_ip_addr(ipaddress):
    scan = api.scan([ipaddress])

def dolly_run(message):

    inputs = tokenizer(message, return_tensors="pt")
    result = model.generate(**inputs)
    return tokenizer.decode(result[0])
     


tools = [
    
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
#    Tool(
#        name="Search",
#        func=search.run,
#        description="useful general questions but not shodan.",
#    ),
    Tool(
        name="Bash",
        func=bash.run,
        description="use this to execute shell commands or git commits",
        ),
#    Tool(
#        name="Google Places",
#        func=bash.run,
#        description="use this to get information about a place, restaurant or hotel..",
#        ),
    
]


#llm_female_refined_llama = LlamaCpp(model_path="./ggml-model-q4_0.bin")
#llm_female_refined_chain_llama = LLMChain(prompt=prompt, llm=llm)

#template = """Question: {question} Answers think step by step."""
#prompt = PromptTemplate(template=template, input_variables=["question"])

#prefix = """The following is a conversation between a human and an AI. The AI is talkative and provides information about a target system, organization and domain. The AI can write code and execute it. If the AI doesn't know the answer to a question, it truthfully says it does not know. You have access to the following tools: """


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

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
agent_chain = initialize_agent(
    tools,
    #llm=ChatOpenAI(temperature=0.0),
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    #agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    #agent= AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
    #ax_iterations=5,
    #arly_stopping_method="generate",
    max_execution_time=15,
    #max_iterations=1,
)

#SMS messaging tools and endpoint


def query_agent(inb_msg: str):
    return str(agent_chain.run(input=inb_msg))
