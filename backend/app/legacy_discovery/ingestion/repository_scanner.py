from pathlib import Path


IGNORED_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".next",
    "dist",
    "build",
    "coverage",
}

LANGUAGE_MAP = {
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
}


def scan_repository(repository_path: str) -> dict:
    root = Path(repository_path)

    if not root.is_dir():
        raise ValueError("Repository directory does not exist")

    languages = set()
    frameworks = set()
    total_files = 0
    file_inventory = []

    for file_path in root.rglob("*"):

        if not file_path.is_file():
            continue

        relative_path = file_path.relative_to(root)

        if any(part in IGNORED_DIRS for part in relative_path.parts):
            continue

        total_files += 1

        extension = file_path.suffix.lower()

        language = LANGUAGE_MAP.get(extension)

        if language:
            languages.add(language)

        file_inventory.append({
            "path": relative_path.as_posix(),
            "extension": extension,
            "language": language or "Unknown",
            "size_bytes": file_path.stat().st_size,
        })

        filename = file_path.name.lower()

        if filename == "requirements.txt":
            frameworks.update(
                detect_python_frameworks(file_path)
            )

        elif filename == "package.json":
            frameworks.update(
                detect_javascript_frameworks(file_path)
            )

        elif filename == "pom.xml":
            frameworks.add("Maven")

        elif filename == "build.gradle":
            frameworks.add("Gradle")

        elif filename == "dockerfile":
            frameworks.add("Docker")

    return {
        "total_files": total_files,
        "languages": sorted(languages),
        "frameworks": sorted(frameworks),
        "file_inventory": file_inventory,
    }


def detect_python_frameworks(file_path: Path) -> set:
    frameworks = set()

    try:
        content = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        ).lower()

        framework_map = {
            "fastapi": "FastAPI",
            "django": "Django",
            "flask": "Flask",
            "langchain": "LangChain",
            "langgraph": "LangGraph",
            "streamlit": "Streamlit",
        }

        for keyword, framework in framework_map.items():
            if keyword in content:
                frameworks.add(framework)

    except OSError:
        pass

    return frameworks


def detect_javascript_frameworks(file_path: Path) -> set:
    import json

    frameworks = set()

    try:
        data = json.loads(
            file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        )

        dependencies = {}

        dependencies.update(data.get("dependencies", {}))
        dependencies.update(data.get("devDependencies", {}))

        framework_map = {
            "react": "React",
            "next": "Next.js",
            "vue": "Vue.js",
            "angular": "Angular",
            "express": "Express.js",
            "nestjs": "NestJS",
            "vite": "Vite",
        }

        for package, framework in framework_map.items():
            if package in dependencies:
                frameworks.add(framework)

    except (OSError, json.JSONDecodeError, TypeError):
        pass

    return frameworks





