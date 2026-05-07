from app import app
from services.storage_service import StorageService
from pathlib import Path


def upload_to_bucket():
    service = StorageService(app)
    image = Path.home() / 'Desktop' / 'dp.jpg'
    with open(image, 'rb') as file:
        file.filename = image.name
        try:
            service.upload_image(file, 'Dogs')
            print("Image Uploaded")
        except Exception as e:
            print(f"Error: {e}")

upload_to_bucket()



