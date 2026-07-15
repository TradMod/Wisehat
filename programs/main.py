import os
from dotenv import load_dotenv
import langchain
from langchain_openai import ChatOpenAI 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
load_dotenv()

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

# prompt template which tells the system about flaggings
# - import the model -
# - basic ai model chat -
# - add a template with a system prompt -
# - take user input -
# - full prompt to the model and fetch the response -

# website page loader and input to the prompt
# -
 
# memory of the chat 
# - 