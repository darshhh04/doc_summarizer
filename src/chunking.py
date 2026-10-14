from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 10000    
CHUNK_OVERLAP = 500  


def split_into_chunks(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n"],         
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_text(text)


def preview_chunks(chunks: list[str]) -> None:
    
    for i, chunk in enumerate(chunks, start=1):
        first_line = chunk.split("\n")[0]
        print(f"Chunk {i}: {len(chunk)} chars | starts with: {first_line[:50]}...")
        if len(chunk) > CHUNK_SIZE * 1.5:
            print("  WARNING: this chunk is much larger than the limit")


if __name__ == "__main__":
    #
    with open("samples/meeting1.txt", encoding="utf-8") as f:
        text = f.read()
    long_text = (text + "\n") * 200     
    chunks = split_into_chunks(long_text)
    print("Total chunks:", len(chunks))
    preview_chunks(chunks)