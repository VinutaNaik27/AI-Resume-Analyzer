from langchain_text_splitters import RecursiveCharacterTextSplitter

HEADINGS = {
    "summary":"summary", "professional summary":"summary", "profile":"summary",
    "objective":"summary", "skills":"skills", "technical skills":"skills",
    "experience":"experience", "work experience":"experience",
    "professional experience":"experience", "internship":"experience",
    "internships":"experience", "projects":"projects", "education":"education",
    "certifications":"certifications", "achievements":"achievements"
}

def create_semantic_chunks(text):
    sections = []
    current = "general"
    content = []

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        heading = HEADINGS.get(line.lower().replace(":", ""))
        if heading:
            if content:
                sections.append((current, "\n".join(content)))
            current = heading
            content = []
        else:
            content.append(line)

    if content:
        sections.append((current, "\n".join(content)))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = []
    for section, value in sections:
        for chunk in splitter.split_text(value):
            if chunk.strip():
                chunks.append({"section": section, "content": chunk})
    return chunks
