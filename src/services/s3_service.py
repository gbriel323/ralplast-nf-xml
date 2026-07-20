import uuid
from datetime import datetime, timezone

import boto3

from config import Config


s3 = boto3.client(
    "s3",
    region_name=Config.AWS_REGION
)


def salvar_no_s3(xml_bytes: bytes) -> dict:

    agora = datetime.now(timezone.utc)


    key = (
        f"nfe/xml/"
        f"{agora.year}/"
        f"{agora.month:02d}/"
        f"{agora.day:02d}/"
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