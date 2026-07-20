import boto3

from decimal import Decimal

from config import Config



dynamodb = boto3.resource(
    "dynamodb",
    region_name=Config.AWS_REGION
)



table = dynamodb.Table(
    "tb-ralplast-nfe-metadata"
)



def convert_decimal(value):

    if isinstance(value, float):

        return Decimal(
            str(value)
        )


    if isinstance(value, dict):

        return {

            key: convert_decimal(val)

            for key, val in value.items()

        }


    if isinstance(value, list):

        return [

            convert_decimal(item)

            for item in value

        ]


    return value




def save_metadata(metadata):


    if not metadata.get(
        "chave_acesso"
    ):

        raise Exception(
            "Chave NF-e obrigatória"
        )


    # ===================================
    # Criar ID DynamoDB
    # ===================================

    metadata["nfe_id"] = (
        metadata["chave_acesso"]
    )



    # ===================================
    # Timestamp
    # ===================================

    from datetime import datetime


    metadata["created_at"] = (
        datetime.utcnow()
        .isoformat()
    )



    # ===================================
    # Converter Decimal
    # ===================================

    item = convert_decimal(
        metadata
    )



    table.put_item(
        Item=item
    )


    return True