from langchain.tools import BaseTool
from math import pi
from typing import Union
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent
from langchain.schema import SystemMessage

class insulin_dose(BaseTool):
    name = "Dose calculator"
    description = "use this tool to calculate your insulin dose based on your carbs"

    def _run(self, params):
        return int(params)

    def _arun(self, params):
        raise NotImplementedError("This tool does not support async")
    
def return_agent(api_key):

    # initialize LLM (we use ChatOpenAI because we'll later define a `chat` agent)
    llm = ChatOpenAI(
            openai_api_key= api_key,
            temperature=0.2,
            model_name='gpt-4'
    )

    # initialize conversational memory
    conversational_memory = ConversationBufferWindowMemory(
            memory_key='chat_history',
            k=5,
            return_messages=True
    )


    tools = [insulin_dose()]

    # initialize agent with tools
    agent = initialize_agent(
        agent='chat-conversational-react-description',
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=10,
        early_stopping_method='generate',
        memory=conversational_memory
    )

    sys_msg = """As a meal prep AI assistant for diabetics, I provide personalized meal suggestions based on a user's glucose level, dietary preferences, budget, and location. I can offer a variety of meals that are suitable for managing diabetes, and upon request, I'll provide detailed ingredient lists along with links to order these ingredients online. My goal is to make meal planning easier, healthier, and more accessible for people with diabetes, ensuring that their nutritional needs are met without sacrificing flavor or variety. I avoid providing medical advice and always encourage consulting with a healthcare professional for personalized dietary guidance. I'm designed to be friendly, supportive, and informative, aiming to simplify the process of finding and preparing diabetes-friendly meals.
    """
    new_prompt = agent.agent.create_prompt(
        system_message=sys_msg,
        tools=[]
    )

    agent.agent.llm_chain.prompt = new_prompt

    return agent
    