import boto3

from config import Config


dynamodb = boto3.resource(
    "dynamodb",
    region_name=Config.AWS_REGION
)


table = dynamodb.Table(
    Config.DYNAMODB_TABLE_NFE
)


def salvar_metadata(item: dict):

    response = table.put_item(
        Item=item
    )

    return response