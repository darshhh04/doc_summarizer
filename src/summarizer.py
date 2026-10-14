from langchain_core.prompts import ChatPromptTemplate

from src.chunking import split_into_chunks
from src.llm_utils import run_step


CHUNK_PROMPT = ChatPromptTemplate.from_template(
    """You are summarizing one part of a meeting transcript.
Write a summary of 6-8 sentences. Keep speaker names.
Always keep: decisions (and who made them), tasks (owner and deadline),
and problems or risks. Do not invent facts.

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


def summarize_chunks(chunks, tracker, progress=None):
    summaries = []
    for i, chunk in enumerate(chunks, start=1):
        print(f"Summarizing chunk {i}/{len(chunks)}...")
        if progress:
            progress(0.1 + 0.5 * (i - 1) / len(chunks), f"Summarizing chunk {i}/{len(chunks)}...")
        summaries.append(run_step(f"chunk_summary_{i}", CHUNK_PROMPT, {"chunk": chunk}, tracker))
    return summaries


def merge_summaries(summaries, tracker):
    joined = "\n\n".join(f"Part {i}: {s}" for i, s in enumerate(summaries, start=1))
    return run_step("global_summary", MERGE_PROMPT, {"summaries": joined}, tracker)