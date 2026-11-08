
import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models import Repository

from app.legacy_discovery.ingestion.zip_extractor import (
    extract_repository,
    MAX_ARCHIVE_SIZE,
)

from app.legacy_discovery.ingestion.repository_scanner import (
    scan_repository,
)

from app.legacy_discovery.schemas.repository import (
    RepositoryUploadResponse,
    RepositoryAnalysis,
)


router = APIRouter()

STORAGE_ROOT = Path("storage/repositories").resolve()


@router.post(
    "/upload",
    response_model=RepositoryUploadResponse,
)
async def upload_legacy_repository(
    tenant_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    repository_id = str(uuid4())
    repository_dir = STORAGE_ROOT / repository_id

    if not tenant_id.strip() or len(tenant_id) > 100:
        raise HTTPException(
            status_code=400,
            detail="Invalid tenant ID",
        )

    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(
            status_code=400,
            detail="Only ZIP files are supported",
        )

    safe_filename = Path(file.filename).name

    repository_name = Path(safe_filename).stem[:200]

    if not repository_name:
        raise HTTPException(
            status_code=400,
            detail="Invalid repository filename",
        )

    try:
        repository_dir.mkdir(parents=True, exist_ok=False)

        zip_path = repository_dir / "source.zip"
        extracted_path = repository_dir / "extracted"

        uploaded_size = 0

        # Save uploaded ZIP in chunks with a size limit.
        with zip_path.open("xb") as destination:

            while True:
                chunk = await file.read(1024 * 1024)

                if not chunk:
                    break

                uploaded_size += len(chunk)

                if uploaded_size > MAX_ARCHIVE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="ZIP archive exceeds 100 MB limit",
                    )

                destination.write(chunk)

        await file.close()

        # Validate that the uploaded file is actually a ZIP.
        import zipfile

        if not zipfile.is_zipfile(zip_path):
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is not a valid ZIP archive",
            )

        # Safely extract the repository.
        extract_repository(
            str(zip_path),
            str(extracted_path),
        )

        # Analyze repository files.
        analysis = scan_repository(
            str(extracted_path),
        )

        if analysis["total_files"] == 0:
            raise HTTPException(
                status_code=400,
                detail="No supported repository files found",
            )

        # Save metadata in PostgreSQL.
        repository = Repository(
            repository_id=repository_id,
            tenant_id=tenant_id,
            repository_name=repository_name,
            original_filename=safe_filename,
            storage_path=str(extracted_path),
            status="uploaded",
            total_files=analysis["total_files"],
            languages=analysis["languages"],
            frameworks=analysis["frameworks"],
            file_inventory=analysis["file_inventory"],
        )

        db.add(repository)
        db.commit()
        db.refresh(repository)

        return RepositoryUploadResponse(
            repository_id=repository.repository_id,
            tenant_id=repository.tenant_id,
            repository_name=repository.repository_name,
            original_filename=repository.original_filename,
            status=repository.status,
            analysis=RepositoryAnalysis(
                total_files=repository.total_files,
                languages=repository.languages,
                frameworks=repository.frameworks,
            ),
            created_at=repository.created_at,
        )

    except HTTPException:
        db.rollback()
        shutil.rmtree(repository_dir, ignore_errors=True)
        raise

    except ValueError as exc:
        db.rollback()
        shutil.rmtree(repository_dir, ignore_errors=True)

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        db.rollback()
        shutil.rmtree(repository_dir, ignore_errors=True)

        raise HTTPException(
            status_code=500,
            detail="Repository ingestion failed",
        ) from exc




