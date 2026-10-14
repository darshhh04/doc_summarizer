from src.extraction import extract, DECISIONS_PROMPT
from src.schemas import DecisionList
from src.tokens import TokenTracker


def test_valid_json_is_parsed(monkeypatch):
    fake = '{"decisions": [{"decision": "Launch on Nov 15", "made_by": "Priya"}]}'
    monkeypatch.setattr("src.extraction.run_step", lambda *args, **kwargs: fake)

    result = extract("decisions", DECISIONS_PROMPT, DecisionList, "notes", TokenTracker())
    assert result.decisions[0].made_by == "Priya"


def test_bad_output_does_not_crash(monkeypatch):
    monkeypatch.setattr("src.extraction.run_step", lambda *args, **kwargs: "not json at all")

    result = extract("decisions", DECISIONS_PROMPT, DecisionList, "notes", TokenTracker())
    assert result.decisions == []       