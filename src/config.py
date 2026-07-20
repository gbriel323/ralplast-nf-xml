from dotenv import load_dotenv
import os


# Carrega .env somente localmente
load_dotenv()


class Config:

    # AWS
    AWS_REGION = os.getenv(
        "AWS_REGION",
        "sa-east-1"
    )


    # S3 - XML original
    S3_BUCKET_XML = os.getenv(
        "S3_BUCKET_XML",
        "ralplast-xml-452408242851-sa-east-1-an"
    )


    # DynamoDB - Metadados NF-e
    DYNAMODB_TABLE_NFE = os.getenv(
        "DYNAMODB_TABLE_NFE",
        "tb-ralplast-nfe-metadata"
    )


    # Ambiente
    ENV = os.getenv(
        "ENV",
        "dev"
    )


    # Logs
    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )