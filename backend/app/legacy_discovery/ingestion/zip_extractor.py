
import os
import shutil
import stat
import zipfile

from pathlib import Path, PurePosixPath


MAX_ARCHIVE_SIZE = 100 * 1024 * 1024
MAX_EXTRACTED_SIZE = 500 * 1024 * 1024
MAX_FILES = 10000
MAX_SINGLE_FILE_SIZE = 50 * 1024 * 1024

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

IGNORED_FILES = {
    ".env",
    ".env.local",
    ".env.production",
    "id_rsa",
    "id_ed25519",
}


def extract_repository(zip_path: str, destination: str) -> int:
    """
    Safely extract a repository ZIP.

    Returns the number of extracted files.
    """

    zip_file_path = Path(zip_path)
    destination_path = Path(destination).resolve()

    if zip_file_path.stat().st_size > MAX_ARCHIVE_SIZE:
        raise ValueError("ZIP archive exceeds 100 MB limit")

    if destination_path.exists():
        shutil.rmtree(destination_path)

    destination_path.mkdir(parents=True, exist_ok=True)

    total_size = 0
    extracted_files = 0

    try:
        with zipfile.ZipFile(zip_file_path, "r") as archive:

            members = archive.infolist()

            if len(members) > MAX_FILES:
                raise ValueError("ZIP contains too many entries")

            for member in members:

                if member.is_dir():
                    continue

                relative_path = PurePosixPath(member.filename)

                if (
                    relative_path.is_absolute()
                    or not relative_path.parts
                    or ".." in relative_path.parts
                    or "\\" in member.filename
                ):
                    raise ValueError("Unsafe ZIP entry detected")

                if "\x00" in member.filename:
                    raise ValueError("Invalid ZIP filename")

                if any(
                    part.lower() in IGNORED_DIRS
                    for part in relative_path.parts[:-1]
                ):
                    continue

                if relative_path.name.lower() in IGNORED_FILES:
                    continue

                unix_mode = member.external_attr >> 16

                if stat.S_ISLNK(unix_mode):
                    raise ValueError("Symbolic links are not allowed")

                if member.file_size > MAX_SINGLE_FILE_SIZE:
                    raise ValueError("Individual file exceeds 50 MB")

                total_size += member.file_size

                if total_size > MAX_EXTRACTED_SIZE:
                    raise ValueError("Extracted repository exceeds 500 MB")

                target_path = (
                    destination_path.joinpath(*relative_path.parts)
                ).resolve()

                if (
                    target_path != destination_path
                    and destination_path not in target_path.parents
                ):
                    raise ValueError("ZIP path traversal detected")

                target_path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                with archive.open(member, "r") as source:
                    with open(target_path, "xb") as target:

                        copied = 0

                        while True:
                            chunk = source.read(1024 * 1024)

                            if not chunk:
                                break

                            copied += len(chunk)

                            if copied > MAX_SINGLE_FILE_SIZE:
                                raise ValueError(
                                    "Extracted file exceeds size limit"
                                )

                            target.write(chunk)

                extracted_files += 1

        return extracted_files

    except Exception:
        shutil.rmtree(destination_path, ignore_errors=True)
        raise


    





