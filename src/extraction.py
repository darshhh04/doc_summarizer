from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from src.llm_utils import run_step
from src.schemas import DecisionList, ActionItemList, RiskList, TopicList


DECISIONS_PROMPT = """Extract every key decision from the meeting notes.
For each decision give the decision and the speaker who made or approved it.
If a name is not clear, use "Unknown". Return an empty list if none."""

ACTIONS_PROMPT = """Extract every action item from the meeting notes.
For each give the task, the owner (person responsible) and the deadline.
Use "Unassigned" if there is no owner and null if there is no deadline."""

RISKS_PROMPT = """Extract every risk, blocker or concern from the meeting notes.
For each give the risk and a severity: Low, Medium or High."""

TOPICS_PROMPT = """Group the meeting content into 2-6 topic clusters.
For each topic give a short name and 1-3 key points."""


def extract(step_name, instruction, model_class, notes, tracker, retries=3):
    
    parser = PydanticOutputParser(pydantic_object=model_class)
    prompt = ChatPromptTemplate.from_template(
        instruction + "\n\n{format_instructions}\n\nMeeting notes:\n{notes}"
    )
    inputs = {"format_instructions": parser.get_format_instructions(), "notes": notes}

    for attempt in range(1, retries + 1):
        raw = run_step(step_name, prompt, inputs, tracker)
        try:
            return parser.parse(raw)
        except Exception as error:
            print(f"  Parse failed for '{step_name}' (attempt {attempt}/{retries}): {error}")

    print(f"  Giving up on '{step_name}', returning an empty result.")
    return model_class()     


def extract_all(notes, tracker):
    return {
        "decisions": extract("decisions", DECISIONS_PROMPT, DecisionList, notes, tracker).decisions,
        "action_items": extract("actions", ACTIONS_PROMPT, ActionItemList, notes, tracker).action_items,
        "risks": extract("risks", RISKS_PROMPT, RiskList, notes, tracker).risks,
        "topics": extract("topics", TOPICS_PROMPT, TopicList, notes, tracker).topics,
    }