
from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".go": "Go",
    ".cs": "C#",
    ".cpp": "C++",
    ".c": "C",
    ".h": "C/C++",
    ".php": "PHP",
    ".rb": "Ruby",
    ".rs": "Rust",
    ".sql": "SQL",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".xml": "XML",
    ".sh": "Shell",
    ".kt": "Kotlin",
    ".swift": "Swift",
}

IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".next",
    "dist",
    "build",
    "coverage",
    "vendor",
}

IGNORED_FILES = {
    ".env",
    ".env.local",
    ".env.production",
    "id_rsa",
    "id_ed25519",
}

MAX_SOURCE_FILE_BYTES = 1_000_000
CHUNK_LINES = 80
CHUNK_OVERLAP = 10


def discover_source_files(repository_path: Path):
    """Find supported source files while excluding generated folders."""

    for file_path in repository_path.rglob("*"):
        if not file_path.is_file():
            continue

        relative_path = file_path.relative_to(repository_path)

        if any(part in IGNORED_DIRECTORIES for part in relative_path.parts):
            continue

        if file_path.name in IGNORED_FILES:
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            if file_path.stat().st_size > MAX_SOURCE_FILE_BYTES:
                continue
        except OSError:
            continue

        yield file_path


def split_into_chunks(source_code: str):
    """Split source code into overlapping line-based chunks."""

    lines = source_code.splitlines()

    if not lines:
        return []

    chunks = []
    start = 0
    chunk_index = 0

    while start < len(lines):
        end = min(start + CHUNK_LINES, len(lines))

        content = "\n".join(lines[start:end]).strip()

        if content:
            chunks.append({
                "chunk_index": chunk_index,
                "start_line": start + 1,
                "end_line": end,
                "content": content,
            })
            chunk_index += 1

        if end == len(lines):
            break

        start = end - CHUNK_OVERLAP

    return chunks


def parse_repository(repository_path: Path):
    """Read supported files and produce searchable code chunks."""

    parsed_chunks = []

    for file_path in discover_source_files(repository_path):
        try:
            source_code = file_path.read_text(
                encoding="utf-8",
                errors="replace",
            )

            # Skip files that appear to contain binary data.
            if "\x00" in source_code:
                continue

            language = SUPPORTED_EXTENSIONS[file_path.suffix.lower()]

            file_chunks = split_into_chunks(source_code)

            for chunk in file_chunks:
                parsed_chunks.append({
                    **chunk,
                    "file_path": str(
                        file_path.relative_to(repository_path)
                    ),
                    "language": language,
                })

        except (OSError, UnicodeError):
            continue

    return parsed_chunks







