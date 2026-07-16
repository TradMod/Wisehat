import os
from dotenv import load_dotenv
import langchain
from langchain_openai import ChatOpenAI 
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.document_loaders import WebBaseLoader
from immunefi_pageloader import immunefi_data
from hackenproof_mcp import hackenproof_data
load_dotenv()

program_name_imu = input("IMU name: ")
result_imu = immunefi_data(program_name_imu)
print(result_imu)

program_name_hp = input("HP name: ")
result_hp = hackenproof_data(program_name_hp)
print(result_hp)

llm = ChatOpenAI(
    model="glm-5.1",
    api_key=os.getenv("OPENCODE_GO_API_KEY"),
    base_url="https://opencode.ai/zen/go/v1",
    temperature=0,
)

history = []

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert AI Bug Bounty Programs' Rules Expert.

        Your responsibilities:
        - Answer accurately and concisely.
        """,
    ),
    MessagesPlaceholder(
        "history"
    ),
    (
        "human",
        """
        {user_input}
        """,
    ),
])

while True:
    user_input = input("Input: ")
    if user_input == "0":
        break
    formatted_prompt = prompt.invoke({
    "history": history[-10:],    
    "user_input": user_input
    })
    response = llm.invoke(formatted_prompt)
    history.append(HumanMessage(content=user_input))
    print(response.content)
    history.append(AIMessage(content=response.content))
print(history)
