import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI 
from langchain_core.prompts import ChatPromptTemplate
from programs.immunefi_loader import immunefi_data
from programs.hackenproof_mcp import hackenproof_data
load_dotenv()

llm = ChatOpenAI(
    model="glm-5.1",
    api_key=os.getenv("OPENCODE_GO_API_KEY"),
    base_url="https://opencode.ai/zen/go/v1",
    temperature=0,
)

SYSTEM_PROMPT = Path("prompts/system_prompt.md").read_text(encoding="utf-8")

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        SYSTEM_PROMPT,
    ),
    (
        "human",
        """
        {llm_prompt}
        """,
    ),
])

def main():
    platform = input("BBP Platform: ")
    program_name = input("BBP Program: ")
    if platform == "Immunefi":
        program_data = immunefi_data(program_name)
    elif platform == "Hackenproof":
        program_data = hackenproof_data(program_name)
    else:
        print(f"Unsupported Platform: {platform}")
        return
    
    formatted_prompt = prompt.invoke({
    "llm_prompt": program_data
    })

    response = llm.invoke(formatted_prompt)
    print(response.content)

if __name__ == "__main__":
    main()