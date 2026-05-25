from pathlib import Path


def load_markdown_files(directory_path: str) -> list[dict]:
    """
    Loads markdown files from a directory.

    Returns a list of documents:
    [
        {
            "title": "ai-advisor-design.md",
            "source_path": "knowledge_base/ai-advisor-design.md",
            "content": "# AI Advisor Design..."
        }
    ]
    """
    directory = Path(directory_path)

    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    documents = []

    for file_path in directory.glob("*.md"):
        content = file_path.read_text(encoding="utf-8").strip()

        if not content:
            continue

        documents.append(
            {
                "title": file_path.name,
                "source_path": str(file_path),
                "content": content,
            }
        )

    return documents