import os
import uuid
from pathlib import Path
from .config import settings

ALLOWED_EXTENSIONS = {".pdf"}

def validate_pdf(filename: str, content_type: str | None) -> bool:
    return Path(filename).suffix.lower() == ".pdf"

def save_file(file_obj, original_filename: str) -> str:
    # Phase 1 fallback: local storage.
    # Production Phase 3 will use S3-compatible cloud object storage.
    if settings.storage_bucket and settings.storage_access_key:
        import boto3
        client = boto3.client(
            "s3",
            endpoint_url=settings.storage_endpoint or None,
            aws_access_key_id=settings.storage_access_key,
            aws_secret_access_key=settings.storage_secret_key,
            region_name=settings.storage_region,
        )
        key = f"uploads/{uuid.uuid4()}-{Path(original_filename).name}"
        client.upload_fileobj(file_obj, settings.storage_bucket, key, ExtraArgs={"ContentType": "application/pdf"})
        return key

    os.makedirs("local_storage", exist_ok=True)
    key = f"uploads/{uuid.uuid4()}-{Path(original_filename).name}"
    path = Path("local_storage") / key
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as out:
        out.write(file_obj.read())
    return key
