import os
from azure.storage.blob import BlobServiceClient
from settings import app_settings

class SafetyDocsBlobClient:
    def __init__(self):
        self.blob_service_client = BlobServiceClient(
            account_url=f"https://{app_settings.storage_account_name}.blob.core.windows.net",
            credential=app_settings.credential
        )
        self.container_client = self.blob_service_client.get_container_client(app_settings.container_name)

    def download_all_files(self):
        blobs = self.container_client.list_blobs()

        for blob in blobs:
            if blob.name.endswith('.pdf'):
                self.download_file(blob.name)

    def download_file(self, filename):
        blob_client = self.container_client.get_blob_client(filename)
        download_file_path = os.path.join(app_settings.download_dir, filename)  
        os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
        
        try:
            if blob_client.exists():
                with open(download_file_path, "wb") as download_file:
                    download_stream = blob_client.download_blob()
                    download_file.write(download_stream.readall())
                print(f"File '{filename}' downloaded successfully to '{download_file_path}'.")
            else:
                print(f"Warning: File '{filename}' not found in the blob storage.")
                
        except Exception as e:
            print(f"Error downloading file '{filename}': {e}")

if __name__ == "__main__":
    safety_docs_client = SafetyDocsBlobClient()
    safety_docs_client.download_all_files()
    safety_docs_client.download_file("Air Brake and Train Handling 8-01-2024.pdf")