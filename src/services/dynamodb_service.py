import boto3

from decimal import Decimal
from zoneinfo import ZoneInfo
from datetime import datetime

from botocore.exceptions import ClientError

from config import Config


dynamodb = boto3.resource(
    "dynamodb",
    region_name=Config.AWS_REGION
)


table = dynamodb.Table(
    "tb-ralplast-nfe-metadata"
)


# ===================================
# Converter float para Decimal
# ===================================

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


# ===================================
# Buscar NF-e
# ===================================

def get_metadata(nfe_id):

    if not nfe_id:

        raise Exception(
            "nfe_id = chave NF-e obrigatória"
        )


    response = table.get_item(

        Key={
            "nfe_id": nfe_id
        }

    )


    return response.get(
        "Item"
    )


# ===================================
# Salvar Metadata
# ===================================

def save_metadata(metadata):

    if not metadata.get(
        "nfe_id"
    ):

        raise Exception(
            "nfe_id = chave NF-e obrigatória"
        )


    # ===================================
    # Timestamp
    # ===================================

    metadata["created_at"] = (

        datetime.now(
            ZoneInfo(
                "America/Sao_Paulo"
            )
        )

        .isoformat()

    )


    # ===================================
    # Converter Decimal
    # ===================================

    item = convert_decimal(
        metadata
    )


    try:

        table.put_item(

            Item=item,

            ConditionExpression=
                "attribute_not_exists(nfe_id)"

        )


    except ClientError as e:


        if (

            e.response[
                "Error"
            ][
                "Code"
            ]

            ==

            "ConditionalCheckFailedException"

        ):

            raise Exception(

                "NF-e já cadastrada no sistema"

            )


        raise


    return True