import os
from threading import Lock

from azure.storage.blob import BlobServiceClient

from app.utils.config import get_config
from app.utils.logger import configure_logger

logger = configure_logger()

# Initialize Azure Blob Storage Client
container_name = get_config("AZURE_CONTAINER_NAME")


class AzureBlobClient:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self._refresh_client()

    def _refresh_client(self):
        connection_string = get_config("AZURE_STORAGE_CONNECTION_STRING")
        if not connection_string:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING is not set in env variables")
        self._client = BlobServiceClient.from_connection_string(connection_string)

    @classmethod
    def get_client(cls) -> BlobServiceClient:
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = AzureBlobClient()

        try:
            # Simple validation by checking account properties
            cls._instance._client.get_account_information()
            return cls._instance._client
        except Exception as e:
            print(f"BlobServiceClient connection invalid, refreshing: {e}")
            with cls._lock:
                cls._instance._refresh_client()
            return cls._instance._client


def upload_influencer_image(influencer_id: int, image_file) -> str:
    """
    Uploads or updates an influencer's image in Azure Blob Storage.
    Args:
        influencer_id (int): Unique ID of the influencer.
        image_file (UploadFile): The image file uploaded by the user.
    Returns:
        str: URL of the uploaded image in Azure Blob Storage.
    """
    try:
        # Generate a consistent filename based on influencer_id
        # file_extension = os.path.splitext(image_file.filename)[1]
        blob_filename = f"influencer_{influencer_id}_image"
        # Get a blob client
        blob_service_client = AzureBlobClient.get_client()
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_filename)
        # Check if the blob already exists and overwrite it
        if blob_client.exists():
            blob_client.delete_blob()
        # Upload the new image
        blob_client.upload_blob(image_file.file, overwrite=True)
        # Construct and return the image URL
        image_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_filename}"
        return image_url
    except Exception as e:
        raise Exception(f"Failed to upload image: {e}")
