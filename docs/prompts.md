# Prompt Templates and Design Reasoning

## 1. Chunk summary prompt (`src/summarizer.py`)
- Asks for 6-8 sentences and tells the model to keep speaker names, decisions, tasks (owner and deadline) and risks.
- Reason: later extraction reads these summaries, so anything dropped here is lost.

## 2. Merge prompt
- Combines the chunk summaries into one executive summary.
- Reason: the model only sees short summaries, so 50,000-word transcripts never hit the context limit.

## 3. Extraction prompts (`src/extraction.py`)
- Separate prompts for decisions, action items, risks and topics.
- Each prompt includes Pydantic format instructions, so the model answers in JSON that matches our schema (structured output constraint).
- Reason: one small task per prompt gives more accurate and easier-to-parse results.

## Iteration log
| Version | Change | Result |
|---|---|---|
| v1 | Chunk prompt asked for 4-6 sentences | Deadlines and owners were sometimes dropped |
| v2 | Asked for 6-8 sentences and told it to keep owners and deadlines | Owners and deadlines kept in summaries |
| v3 | Turned off thinking tokens, skipped merge for single chunk | Far fewer output tokens, same quality |