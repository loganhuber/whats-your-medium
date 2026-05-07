from uuid import uuid4
import boto3

class StorageService:
    def __init__(self, app):
        self.bucket = app.config["DO_SPACES_BUCKET"]
        self.region = app.config["DO_SPACES_REGION"]
        self.client = boto3.client(
            "s3",
            region_name=app.config["DO_SPACES_REGION"],
            endpoint_url=(
                f"https://"
                f"{app.config['DO_SPACES_REGION']}"
                ".digitaloceanspaces.com"
            ),
            aws_access_key_id=app.config["DO_SPACES_KEY"],
            aws_secret_access_key=app.config["DO_SPACES_SECRET"],
        )

    def upload_image(self, file, category, filename=None):
        if filename is None:
            filename = file.filename
        suffix = filename.rsplit(".", 1)[1]

        key = (
            f"whats-your-medium/"
            f"uploads/"
            f"{category}/"
            f"{uuid4()}.{suffix}"
        )

        self.client.upload_fileobj(
            file,
            self.bucket,
            key,
            ExtraArgs={"ACL": "public-read"}
        )

        return key

    def delete_image(self, key):
        self.client.delete_object(
            Bucket=self.bucket,
            Key=key
        )
