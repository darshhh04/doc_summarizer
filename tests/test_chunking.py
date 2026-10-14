from src.chunking import split_into_chunks


def test_chunks_never_split_a_speaker_turn():
    turns = [f"Speaker{i}: This is sentence number {i}." for i in range(1000)]
    chunks = split_into_chunks("\n".join(turns))

    assert len(chunks) > 1
    for chunk in chunks:
        for line in chunk.split("\n"):
            assert line in turns        