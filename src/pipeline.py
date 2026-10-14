from src.chunking import split_into_chunks
from src.summarizer import summarize_chunks, merge_summaries
from src.extraction import extract_all
from src.schemas import MeetingResult
from src.tokens import TokenTracker


def process_transcript(text: str, name: str = "transcript", progress=None):
    
    tracker = TokenTracker(name)

    if progress:
        progress(0.05, "Splitting transcript into chunks...")
    chunks = split_into_chunks(text)

    chunk_summaries = summarize_chunks(chunks, tracker, progress)

    if len(chunk_summaries) == 1:
        executive_summary = chunk_summaries[0]    
        notes = executive_summary
    else:
        if progress:
            progress(0.7, "Creating executive summary...")
        executive_summary = merge_summaries(chunk_summaries, tracker)
        notes = executive_summary + "\n\n" + "\n\n".join(chunk_summaries)

    if progress:
        progress(0.8, "Extracting decisions, actions, risks and topics...")
    extracted = extract_all(notes, tracker)

    result = MeetingResult(summary=executive_summary, **extracted)
    tracker.save()

    if progress:
        progress(1.0, "Done!")
    return result, tracker.summary()


if __name__ == "__main__":
   
    with open("samples/meeting1.txt", encoding="utf-8") as f:
        text = f.read()
    result, usage = process_transcript(text, "meeting1.txt")
    print(result.model_dump_json(indent=2))
    print("\nToken usage:", usage)