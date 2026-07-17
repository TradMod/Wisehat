import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI 
from langchain_core.prompts import ChatPromptTemplate
from programs.immunefi_loader import immunefi_data
from programs.hackenproof_mcp import hackenproof_data
load_dotenv()


class WiseHatRecommendation(BaseModel):
    rating: float
    verdict: str
    summary: str

class WiseHatReport(BaseModel):
    platform_name: str
    program_name: str
    wisehat_recommendation: WiseHatRecommendation
    program_overview: str
    mandatory_requirements: list[str]
    green_flags: list[str]
    red_flags: list[str]
    scope_and_impact_analysis: list[str]
    other_things_to_consider: list[str]
    hunter_tips: list[str]
    before_you_hunt_checklist: list[str]

llm = ChatOpenAI(
    model="glm-5.2",
    api_key=os.getenv("OPENCODE_GO_API_KEY"),
    base_url="https://opencode.ai/zen/go/v1",
    temperature=0,
)
structured_llm = llm.with_structured_output(WiseHatReport)

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

chain = prompt | structured_llm

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

    response: WiseHatReport = structured_llm.invoke(formatted_prompt)
    print(response.model_dump_json(indent=4))

if __name__ == "__main__":
    main()