from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.config import get_llm
from src.chunking import split_into_chunks


CHUNK_PROMPT = ChatPromptTemplate.from_template(
    """You are summarizing one part of a meeting transcript.
Write a short summary (4-6 sentences). Keep speaker names.
Mention decisions, tasks and problems if present. Do not invent facts.

Transcript part:
{chunk}

Summary:"""
)


MERGE_PROMPT = ChatPromptTemplate.from_template(
    """Below are summaries of consecutive parts of one meeting.
Combine them into one clear executive summary (6-10 sentences).
Remove repetition and keep the order of events.

Part summaries:
{summaries}

Executive summary:"""
)


def summarize_chunks(chunks: list[str]) -> list[str]:
    chain = CHUNK_PROMPT | get_llm() | StrOutputParser()
    summaries = []
    for i, chunk in enumerate(chunks, start=1):
        print(f"Summarizing chunk {i}/{len(chunks)}...")
        summaries.append(chain.invoke({"chunk": chunk}))
    return summaries


def merge_summaries(summaries: list[str]) -> str:
    chain = MERGE_PROMPT | get_llm() | StrOutputParser()
    joined = "\n\n".join(f"Part {i}: {s}" for i, s in enumerate(summaries, start=1))
    return chain.invoke({"summaries": joined})


def create_executive_summary(text: str) -> str:
    chunks = split_into_chunks(text)
    summaries = summarize_chunks(chunks)
    return merge_summaries(summaries)


if __name__ == "__main__":
  
    with open("samples/meeting1.txt", encoding="utf-8") as f:
        text = f.read()
    print(create_executive_summary(text))