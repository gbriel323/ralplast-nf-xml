from dotenv import load_dotenv
import os

load_dotenv()


class Config:

    # AWS
    AWS_REGION = "sa-east-1"

    # Bucket S3
    S3_BUCKET_XML = "ralplast-xml-452408242851-sa-east-1-an"

    # Ambiente
    ENV = "dev"

    # Logs
    LOG_LEVEL = "INFO"