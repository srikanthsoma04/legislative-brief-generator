import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage

load_dotenv()

BRIEF_PROMPT = PromptTemplate(
    input_variables=["legislator_name", "state", "party", "committees", "voting_records"],
    template="""
You are a civic data analyst specializing in climate policy.

Based on the following voting records, generate a concise one-page legislative brief 
summarizing this legislator's climate policy positions.

Legislator: {legislator_name}
State: {state}
Party: {party}
Committees: {committees}

Voting Records:
{voting_records}

Generate a structured brief with the following sections:
1. Climate Position (Strong Supporter / Moderate / Opponent)
2. Confidence Level (High / Medium / Low)
3. Key Votes summary (list format)
4. 2-3 sentence narrative summary of their climate stance
5. Recommended Engagement level (High Priority / Medium / Low Priority)

Keep the brief factual, concise, and actionable.
"""
)

def generate_brief(legislator: dict, voting_records: list) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in environment.")
    llm = ChatAnthropic(
        model="claude-opus-4-5",
        anthropic_api_key=api_key,
        max_tokens=1000
    )
    prompt = BRIEF_PROMPT.format(
        legislator_name=legislator["name"],
        state=legislator["state"],
        party=legislator["party"],
        committees=", ".join(legislator.get("committees", [])),
        voting_records="\n".join(voting_records)
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content