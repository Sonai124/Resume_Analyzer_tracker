import re
from io import BytesIO
from pypdf import PdfReader


def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    text = "\n".join(parts)

    # remove soft hyphen (very common in PDFs)
    text = text.replace("\u00ad", "")

    # join hyphenated line breaks: "bench-\nmarked" -> "benchmarked"
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

    # normalize whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)

    # sometimes PDFs split single words oddly: "c i r q" -> "cirq"
    text = re.sub(r"\b([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\b",
                  lambda m: (m.group(1) + m.group(2) + m.group(3) + m.group(4)),
                  text)

    return text.strip()