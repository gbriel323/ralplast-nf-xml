import uuid
from datetime import datetime

import boto3

from config import Config

# Cliente S3
s3 = boto3.client(
    "s3",
    region_name=Config.AWS_REGION
)


def salvar_no_s3(xml_bytes: bytes) -> dict:
    """
    Salva um XML no Amazon S3.

    Args:
        xml_bytes (bytes): Conteúdo do arquivo XML.

    Returns:
        dict: Informações do arquivo salvo.
    """

    agora = datetime.utcnow()

    key = (
        f"uploads/"
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
        "key": key,
        "url": f"https://{Config.S3_BUCKET_XML}.s3.{Config.AWS_REGION}.amazonaws.com/{key}"
    }