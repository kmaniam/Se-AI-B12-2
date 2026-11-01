
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
KB_DIR = BASE_DIR / "knowledge_base"

STOP_WORDS = {
    "the", "is", "a", "an", "and", "or",
    "to", "of", "in", "for", "with", "on",
    "my", "can", "how", "what", "when"
}


def tokenize(text):
    words = set(re.findall(r"\b[a-z0-9]+\b", text.lower()))
    return words - STOP_WORDS


def search_kb(query, max_results=5):

    query_words = tokenize(query)

    if not query_words:
        return []

    results = []

    for file_path in KB_DIR.glob("*.md"):

        content = file_path.read_text(encoding="utf-8")

        # Split document into sections using Markdown headings
        sections = re.split(
            r"(?m)(?=^#{1,3}\s+)",
            content
        )

        for section in sections:

            section = section.strip()

            if not section:
                continue

            section_words = tokenize(section)
            matches = query_words.intersection(section_words)

            if matches:

                score = len(matches) / len(query_words)

                results.append({
                    "source": file_path.name,
                    "content": section,
                    "matched_keywords": sorted(matches),
                    "score": round(score, 2)
                })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:max_results]


if __name__ == "__main__":

    query = "refund processing damaged product"

    results = search_kb(query)

    print("\nKnowledge Base Search Results\n")

    for result in results:

        print("Source:", result["source"])
        print("Score:", result["score"])
        print("Matched:", result["matched_keywords"])
        print("Content:", result["content"])
        print("-" * 60)
