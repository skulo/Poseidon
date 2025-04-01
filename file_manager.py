from io import BytesIO
from pathlib import Path
import os
import boto3
from fastapi.responses import FileResponse, StreamingResponse

class FileManager:
    def __init__(self):
        from dotenv import load_dotenv

        load_dotenv()
        self.files_dir = "files"
        self.environment = os.getenv('ENVIRONMENT')
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.region_name = os.getenv('AWS_REGION_NAME')
        self.s3_bucket_name = os.getenv('S3_BUCKET_NAME')

        if self.environment == "EC2":
            self.is_local_storage = False
            self.s3 = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region_name
            )
        else:
            self.is_local_storage = True
            os.makedirs(self.files_dir, exist_ok=True)

    def _sanitize_filename(self, filename: str) -> str:
        """Eltávolítja a 'files/' vagy 'files\\' prefixet a fájlnévből"""
        return filename.replace("files/", "").replace("files\\", "")

    def _get_safe_path(self, filename: str) -> str:
        """Biztonságos útvonalat ad vissza egy fájlhoz (csak a 'files' mappán belül)"""
        filename = self._sanitize_filename(filename)
        safe_path = Path(self.files_dir) / filename
        safe_path = safe_path.resolve()
        if not str(safe_path).startswith(str(Path(self.files_dir).resolve())):
            raise ValueError("Érvénytelen fájlnév (path traversal gyanú)")
        return str(safe_path)

    async def save_file(self, filename: str, file):
        if self.is_local_storage:
            file_path = self._get_safe_path(filename)
            with open(file_path, "wb") as f:
                f.write(await file.read())
            return file_path
        else:
            self.s3.upload_fileobj(file.file, self.s3_bucket_name, filename)
            return f"https://{self.s3_bucket_name}.s3.{self.region_name}.amazonaws.com/{filename}"

    async def get_file(self, filename: str):
        if self.is_local_storage:
            try:
                file_path = self._get_safe_path(filename)
                if os.path.exists(file_path):
                    return FileResponse(file_path, media_type="application/octet-stream", filename=os.path.basename(file_path))
                else:
                    return {"error": "File not found"}
            except Exception as e:
                return {"error": str(e)}
        else:
            try:
                file_obj = self.s3.get_object(Bucket=self.s3_bucket_name, Key=filename)
                file_content = file_obj['Body'].read()
                return StreamingResponse(BytesIO(file_content), media_type="application/octet-stream",
                                         headers={"Content-Disposition": f"attachment; filename={filename}"})
            except Exception as e:
                return {"error": str(e)}

    async def delete_file(self, filename: str):
        if self.is_local_storage:
            try:
                file_path = self._get_safe_path(filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    return {"message": f"File {filename} deleted successfully from local storage."}
                return {"error": "File not found"}
            except Exception as e:
                return {"error": str(e)}
        try:
            self.s3.delete_object(Bucket=self.s3_bucket_name, Key=filename)
            return {"message": f"File {filename} deleted successfully from S3."}
        except Exception as e:
            return {"error": str(e)}

    async def get_file_content(self, filename: str) -> bytes:
        if self.is_local_storage:
            try:
                file_path = self._get_safe_path(filename)
                with open(file_path, "rb") as f:
                    return f.read()
            except Exception as e:
                raise FileNotFoundError(f"Nem sikerült megnyitni a fájlt: {e}")
        else:
            file_obj = self.s3.get_object(Bucket=self.s3_bucket_name, Key=filename)
            return file_obj['Body'].read()
