from src.pipeline import process_transcript


def fake_run_step(step_name, prompt, inputs, tracker, retries=3):
    tracker.add(step_name, 10, 5)
    if step_name == "decisions":
        return '{"decisions": [{"decision": "Launch Nov 15", "made_by": "Priya"}]}'
    if step_name == "actions":
        return '{"action_items": [{"task": "Release notes", "owner": "Rahul", "deadline": "Friday"}]}'
    if step_name == "risks":
        return '{"risks": [{"risk": "API unstable", "severity": "High"}]}'
    if step_name == "topics":
        return '{"topics": [{"name": "Launch", "points": ["Date set"]}]}'
    return "Fake summary text."


def test_full_pipeline_with_fake_llm(monkeypatch):
    monkeypatch.setattr("src.summarizer.run_step", fake_run_step)
    monkeypatch.setattr("src.extraction.run_step", fake_run_step)
    monkeypatch.setattr("src.tokens.TokenTracker.save", lambda self, path="": None)

    result, usage = process_transcript("Priya: Hello.\nRahul: Hi.", "test.txt")

    assert result.summary == "Fake summary text."
    assert result.decisions[0].made_by == "Priya"
    assert result.action_items[0].owner == "Rahul"
    assert result.risks[0].severity == "High"
    assert usage["calls"] == 5         