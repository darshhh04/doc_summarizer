import io
import re
import fitz                    
from docx import Document        


SPEAKER_PATTERN = re.compile(r"^\s*\[?([A-Za-z][A-Za-z .'-]{0,30})\]?\s*[:\-]\s*(.+)$")


def extract_text(file_bytes: bytes, filename: str) -> str:
    
    name = filename.lower()

    if name.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")

    if name.endswith(".docx"):
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs)

    if name.endswith(".pdf"):
        pdf = fitz.open(stream=file_bytes, filetype="pdf")
        return "\n".join(page.get_text() for page in pdf)

    raise ValueError("Unsupported file type. Use .txt, .docx or .pdf")


def normalize_transcript(text: str) -> str:
    
    turns = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        match = SPEAKER_PATTERN.match(line)
        if match:                                 
            turns.append(f"{match.group(1).strip()}: {match.group(2).strip()}")
        elif turns:                                 
            turns[-1] += " " + line
        else:
            turns.append(line)

    return "\n".join(turns)


def word_count(text: str) -> int:
    return len(text.split())


if __name__ == "__main__":
   
    with open("samples/meeting1.txt", "rb") as f:
        raw = extract_text(f.read(), "meeting1.txt")
    clean = normalize_transcript(raw)
    print(clean)
    print("\nWords:", word_count(clean))