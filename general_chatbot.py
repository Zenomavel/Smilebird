# Dental Clinic Rule-Based Chatbot with Math Support and Wikipedia Integration
import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMMathChain, LLMChain
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import Tool, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler

st.set_page_config(page_title="DentalBot Assistant")
st.title("🦷 DentalBot Assistant")

# Sidebar: API Key
api_key = st.sidebar.text_input("🔑 Enter your Groq API key", type="password")
if not api_key:
    st.info("Please enter your Groq API key to proceed.")
    st.stop()

# LLM Setup
llm = ChatGroq(groq_api_key=api_key, model="Gemma2-9b-It")

# Prompt Template
prompt_template = """
You are an agent named DentalBot designed to assist with dental-related FAQs.

Respond clearly, professionally. 
Provide the best answer using your knowledge or search tools.

Question: {question}
Answer:
"""

prompt = PromptTemplate(input_variables=['question'], template=prompt_template)

# Tools
wiki_wrap = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=300)

wiki_tool = Tool(name="Wikipedia", func=wiki_wrap.run, description="Use for general queries")
search_tool = DuckDuckGoSearchRun(name="WebSearch")

faq_bot = LLMChain(llm=llm, prompt=prompt)
reasoning_tool = Tool(name="DentalReasoner", func=faq_bot.run, description="Use for dental and general queries")

# Agent Initialization
agent = initialize_agent(
    tools=[wiki_tool, search_tool, reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# Session Initialization
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Welcome to DentalBot! 🦷\n\nHow can I assist you today?"}
    ]

# Chat UI Loop
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Type your question, e.g., What are your working hours?")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = agent.run(st.session_state["messages"], callbacks=[st_cb])
        st.session_state["messages"].append({"role": "assistant", "content": response})
        st.success(response)
