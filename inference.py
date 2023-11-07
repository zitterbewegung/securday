import ipaddress, os, re, socket
from transformers import AutoTokenizer, AutoModelForCausalLM
from shodan import Shodan

import pwnlib
from langchain.chat_models import ChatOpenAI

# import cve_searchsploit as CS
from langchain.docstore import Wikipedia

from langchain.llms import OpenAI, PromptLayerOpenAI
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from langchain.agents import Tool, AgentType, tool
from langchain.chains import SimpleSequentialChain
from langchain.memory import ConversationBufferMemory
from langchain_experimental.smart_llm import SmartLLMChain
from langchain_experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)

# from langchain.experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from langchain.agents import load_tools, initialize_agent
from langchain.agents.react.base import DocstoreExplorer
from langchain.agents.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain.agents import Tool, AgentExecutor
from langchain_experimental.utilities import PythonREPL
from langchain.tools import ShellTool
from langchain.tools.ifttt import IFTTTWebhook
from langchain.utilities import (
    WikipediaAPIWrapper,
    TextRequestsWrapper,
)
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.llms import LlamaCpp
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.tools import ShellTool
import vt

memory = ConversationBufferMemory()
wolfram = WolframAlphaAPIWrapper()
wikipedia = WikipediaAPIWrapper()
python_repl =  PythonREPLTool()
requests = TextRequestsWrapper()
shodan_api = Shodan(os.environ.get("SHODAN_API_KEY"))
virus_total_client = vt.Client(os.environ.get("VIRUS_TOTAL"))


def hostname(hostname: str) -> str:
    """useful when you need to get the ipaddress associated with a hostname"""
    try:
        ip = ipaddress.ip_address(addr)
        return ip
    except ValueError:
        return "Invalid ip address"


def subset_shodan(addr: str):
    # ipv4_extract_pattern = "(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
    # extracted_ip = re.findall(ipv4_extract_pattern, addr)[0]
    # if ipaddress.ip_address(extracted_ip).is_private:
    #    return "This is a private ip address."
    addr = addr.replace("scan ", "")
    try:
        host = shodan_api.host(addr)
    except Exception as e:
        return "Shodan has no info"
    ports = ""
    for i in host["data"]:
        ports += "Port {} \n".format(i["port"])

    return """
    IP: {}
    Organization: {}
    Operating System: {}
    Country: {}
    Location: Lat {} Long {}
    Asn: {}
    Transport: {}
    Port: {}
    """.format(
        host["ip_str"],
        host.get("org", "n/a"),
        host.get("os", "n/a"),
        host.get("country_name", "n/a"),
        host.get("lat", "n/a"),
        host.get("long", "n/a"),
        host.get("asn", "n/a"),
        host.get("transport", "n/a"),
        ports,
    )

def shell_wrapper(query: str):
    shell_tool.run({"commands": [query]})
    
def virus_total(url: str):
	"""Takes a URL and aggregates the result of malware on the site."""
	url_id = vt.url_id(url)
	url = virus_total_client.get_object("/urls/{}", url_id)

	analysis = url.last_analysis_stats
	
	return """File fetched from URL is
	harmess {},
	malicious {},
	suspicious {}
	. """.format(analysis.get('harmless'),
				 analysis.get("malicious"),
				 analysis.get("suspicious"),)

def scan_ip_addr(ipaddress):
    scan = api.scan([ipaddress])
    return host.get("port", "n/a")


def phone_info(phone_number: str) -> str:
    import http.client

    conn = http.client.HTTPSConnection("api.trestleiq.com")

    conn.request(
        "GET",
        "/3.0/phone_intel?api_key=SOME_STRING_VALUE&phone={}&phone.country_hint=US".format(
            phone_number
        ),
    )

    res = conn.getresponse()
    data = res.read()

    phone_intel_result_payload = data.decode("utf-8")

    return result_payload





tools = [
    Tool(
        name="trestle",
        func=hostname,
        description="useful when you need lookup a hostname given an ip address.",
    ),
	Tool(
	    name="virus_total",
	    func=virus_total,
	    description="used to figure out if a downloaded file has malware or is a virus.",
	),
    Tool(
        name="shodan",
        func=subset_shodan,
        description="useful when you need to figure out information about ip address.",
    ),
    Tool(
        name="wolfram",
        func=wolfram.run,
        description="useful for calculations and mathematical quesions.",
    ),
    Tool(
        name="python_repl",
        func=python_repl,
        description="use this when asked about writing code.",
    ),
    Tool(
        name="ShellTool",
        func=shell_wrapper,
        description="use this to execute shell commands or to find out ip addresses from hostnames",
    ),
]


prompt = """The following is a conversation between a human and an AI. The AI is talkative and provides information about a target system, organization and domain. A user will give information about a hostname or an ip address.  The AI can write code and execute it.  If the AI doesn't know the answer to a question, it truthfully says it does not know. You have access to the following tools: """


#suffix = (
#    "Begin!\n\nPrevious conversation history:\n{chat_history}\n\nNew input: {inp#ut}\n{agent_scratchpad}"
#    ""
#)

message_history = RedisChatMessageHistory(
    url="redis://localhost:6379/0", ttl=600, session_id="my-session"
)

memory = ConversationBufferMemory(
    memory_key="chat_history", chat_memory=message_history
)

llm = ChatOpenAI(temperature=0, model="gpt-4")
#chain = SmartLLMChain(llm=llm, prompt=prompt, n_ideas=3, verbose=True)

def _handle_error(error) -> str:
    return str(error)[:50]


# model = ChatOpenAI(temperature=0)
# planner = load_chat_planner(model)
# executor = load_agent_executor(model, tools, verbose=True)
# agent = PlanAndExecute(memory=memory, planner=planner, executor=executor, verbose=True)

agent_chain = initialize_agent(
    tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    # max_iterations=30,
    # early_stopping_method="generate",
    memory=memory,
    handle_parsing_errors=True,
    max_tokens=30000, #Giving a maximum of 2768 for queries by the agent. 
)

# local_agent_chain = initialize_agent(
#     tools,
#     llm=local_llm,
#     agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     #agent  = AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
#     #agent = AgentType.OPENAI_FUNCTIONS,
#     verbose=True,
#     #max_iterations=30,
#     #early_stopping_method="generate",
#     memory=memory,
#     handle_parsing_errors=True,
#     max_tokens=4000

# )

# SMS messaging tools and endpoint


def query_agent(query_str: str):
    try:
        response = agent_chain.run(input=query_str)

    except ValueError as e:
        response = str(e)
        if not response.startswith("Could not parse LLM output: `"):
            raise e
        response = response.removeprefix("Could not parse LLM output: `").removesuffix(
            "`"
        )
    return str(response)
