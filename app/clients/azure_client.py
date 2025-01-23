from io import BytesIO
from threading import Lock

from PIL import Image
from azure.storage.blob import BlobServiceClient

from app.utils.logger import configure_logger

logger = configure_logger()

# Initialize Azure Blob Storage Client
# container_name = get_config("AZURE_CONTAINER_NAME")
# connection_string = get_config("AZURE_STORAGE_CONNECTION_STRING")

container_name = "profile-picture"
connection_string = "DefaultEndpointsProtocol=https;AccountName=nextreachblob;AccountKey=yAOzUPyHmPJyBoTj702xd/pvoKX9PWG9ZSxu0fg7u6mtOpy9dQ5X2cMGnQ9uG0xPxzffrhgSuq8E+AStyUeP5g==;EndpointSuffix=core.windows.net"


class AzureBlobClient:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self._refresh_client()

    def _refresh_client(self):
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
    Uploads or updates an influencer's image in Azure Blob Storage after cropping it to a square and compressing it.
    Args:
        influencer_id (int): Unique ID of the influencer.
        image_file (UploadFile): The image file uploaded by the user.
    Returns:
        str: URL of the uploaded image in Azure Blob Storage.
    """
    try:
        # Open the uploaded image
        image = Image.open(image_file.file)

        # Ensure the image is a square by cropping from the center
        width, height = image.size
        if width != height:
            new_size = min(width, height)  # Use the smaller dimension
            left = (width - new_size) / 2
            top = (height - new_size) / 2
            right = (width + new_size) / 2
            bottom = (height + new_size) / 2
            image = image.crop((left, top, right, bottom))  # Crop to center square

        # Compress the image to ensure size is under 300KB
        compressed_image = BytesIO()
        quality = 95  # Start with high quality
        for quality in range(95, 30, -5):  # Gradually reduce quality
            compressed_image.seek(0)  # Reset the buffer for each iteration
            compressed_image.truncate(0)  # Clear the contents of the buffer
            image.save(compressed_image, format="JPEG", quality=quality)
            if compressed_image.tell() <= 400 * 1024:  # Check if size is less than 400KB
                break

        compressed_image.seek(0)  # Reset the pointer to the start of the file

        # Generate a consistent filename based on influencer_id
        blob_filename = f"influencer_{influencer_id}_image"

        # Get a blob client
        blob_service_client = AzureBlobClient.get_client()
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_filename)

        # Check if the blob already exists and overwrite it
        if blob_client.exists():
            blob_client.delete_blob()

        # Upload the resized and compressed image
        blob_client.upload_blob(compressed_image, overwrite=True)

        # Construct and return the image URL
        image_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_filename}"
        return image_url
    except Exception as e:
        raise Exception(f"Failed to upload image: {e}")
