from supabase import create_client, Client
from app.core.logging import get_logger

logger = get_logger(__name__)

from app.core.config import settings

class SupabaseClient:
    def __init__(
        self,
        url: str = settings.SUPABASE_URL,
        key: str = settings.SUPABASE_KEY,
        storage_bucket: str = "default",
    ):
        try:
            self.client: Client = create_client(url, key)
            self.storage = self.client.storage.from_(storage_bucket)
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {str(e)}")
            raise ConnectionError(f"Failed to connect to Supabase: {str(e)}")

    def upload_file(self, file_path: str, file_name: str) -> str:
        """Upload a file to Supabase storage.
        
        Args:
            file_path: Path to the file to upload
            file_name: Name to store the file as
            
        Returns:
            Public URL of the uploaded file
        """
        try:
            with open(file_path, 'rb') as f:
                self.storage.upload(file_name, f)
            return self.storage.get_public_url(file_name)
        except Exception as e:
            logger.error(f"Failed to upload file {file_name}: {str(e)}")
            raise RuntimeError(f"Failed to upload file: {str(e)}")

    def download_file(self, file_name: str, destination: str) -> None:
        """Download a file from Supabase storage.
        
        Args:
            file_name: Name of file to download
            destination: Path where to save the downloaded file
        """
        try:
            with open(destination, 'wb') as f:
                data = self.storage.download(file_name)
                f.write(data)
        except Exception as e:
            logger.error(f"Failed to download file {file_name}: {str(e)}")
            raise RuntimeError(f"Failed to download file: {str(e)}")

    def delete_file(self, file_name: str) -> None:
        """Delete a file from Supabase storage.
        
        Args:
            file_name: Name of file to delete
        """
        try:
            self.storage.remove([file_name])
        except Exception as e:
            logger.error(f"Failed to delete file {file_name}: {str(e)}")
            raise RuntimeError(f"Failed to delete file: {str(e)}")

    def get_file_url(self, file_name: str) -> str:
        """Get public URL for a file.
        
        Args:
            file_name: Name of the file
            
        Returns:
            Public URL of the file
        """
        try:
            return self.storage.get_public_url(file_name)
        except Exception as e:
            logger.error(f"Failed to get URL for file {file_name}: {str(e)}")
            raise RuntimeError(f"Failed to get file URL: {str(e)}")
