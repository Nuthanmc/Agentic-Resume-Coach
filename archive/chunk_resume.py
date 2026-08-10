import fitz

PDF_PATH = r"D:\Resume RAG\data\My_Resume (1).pdf"

pdf = fitz.open(PDF_PATH)

text = ""

for page in pdf:
    text += page.get_text()


def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks


chunks = chunk_text(text)

print(f"Total Chunks: {len(chunks)}")

for i, chunk in enumerate(chunks):
    print(f"\n----- CHUNK {i+1} -----")
    print(chunk[:200])