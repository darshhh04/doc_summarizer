from src.chunking import split_into_chunks
from src.summarizer import summarize_chunks, merge_summaries
from src.extraction import extract_all
from src.schemas import MeetingResult
from src.tokens import TokenTracker


def process_transcript(text: str, name: str = "transcript"):
    
    tracker = TokenTracker(name)

    chunks = split_into_chunks(text)
    chunk_summaries = summarize_chunks(chunks, tracker)
    executive_summary = merge_summaries(chunk_summaries, tracker)

    notes = executive_summary + "\n\n" + "\n\n".join(chunk_summaries)
    extracted = extract_all(notes, tracker)

    result = MeetingResult(summary=executive_summary, **extracted)
    tracker.save()
    return result, tracker.summary()


if __name__ == "__main__":
    
    with open("samples/meeting1.txt", encoding="utf-8") as f:
        text = f.read()
    result, usage = process_transcript(text, "meeting1.txt")
    print(result.model_dump_json(indent=2))
    print("\nToken usage:", usage)