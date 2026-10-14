import pytest
from src.ingestion import extract_text, normalize_transcript, word_count


def test_txt_is_read():
    assert extract_text(b"Hello there", "a.txt") == "Hello there"


def test_unsupported_file_type():
    with pytest.raises(ValueError):
        extract_text(b"data", "a.png")


def test_continuation_line_is_joined_to_speaker():
    raw = "Priya: Rahul, please finish\nthe notes by Friday.\nRahul: Okay."
    clean = normalize_transcript(raw)
    assert clean.split("\n")[0] == "Priya: Rahul, please finish the notes by Friday."
    assert len(clean.split("\n")) == 2


def test_word_count():
    assert word_count("one two three") == 3