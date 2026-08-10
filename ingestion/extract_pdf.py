import fitz

PDF_PATH = r"D:\Resume RAG\data\My_Resume (1).pdf"

pdf = fitz.open(PDF_PATH)

text = ""

for page in pdf:
    text += page.get_text()

print("=" * 50)
print("RESUME TEXT")
print("=" * 50)
print(text[:3000])  # first 3000 chars
print("\nTotal Characters:", len(text))