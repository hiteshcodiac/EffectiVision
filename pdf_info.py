from fastapi import UploadFile, File
import os
import shutil
import uuid

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


async def upload_pdf_file(file: UploadFile):

    if file.content_type != "application/pdf":
        return {
            "success": False,
            "error": "Only PDF files are allowed."
        }

    pdf_id = str(uuid.uuid4())

    filename = f"{pdf_id}.pdf"

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "success": True,
        "pdf_id": pdf_id,
        "filename": file.filename
    }


def get_pdf_path(pdf_id):

    return os.path.join(
        UPLOAD_FOLDER,
        f"{pdf_id}.pdf"
    )