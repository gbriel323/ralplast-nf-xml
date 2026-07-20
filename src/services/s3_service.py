import uuid
from datetime import datetime, timezone

import boto3

from config import Config


s3 = boto3.client(
    "s3",
    region_name=Config.AWS_REGION
)


def save_xml(xml_bytes: bytes) -> dict:

    now = datetime.now(timezone.utc)


    key = (
        f"nfe/xml/"
        f"{now.year}/"
        f"{now.month:02d}/"
        f"{now.day:02d}/"
        f"{uuid.uuid4()}.xml"
    )


    s3.put_object(
        Bucket=Config.S3_BUCKET_XML,
        Key=key,
        Body=xml_bytes,
        ContentType="application/xml"
    )


    return {
        "bucket": Config.S3_BUCKET_XML,
        "key": key
    }