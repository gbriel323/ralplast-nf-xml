import boto3

from decimal import Decimal

from config import Config



# ==========================================
# DynamoDB Client
# ==========================================

dynamodb = boto3.resource(
    "dynamodb",
    region_name=Config.AWS_REGION
)



table = dynamodb.Table(
    "tb-ralplast-nfe-metadata"
)



# ==========================================
# Converter tipos para DynamoDB
# ==========================================

def convert_decimal(value):

    """
    DynamoDB boto3 não aceita float.
    Converte automaticamente para Decimal.
    """


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



# ==========================================
# Salvar Metadata NF-e
# ==========================================

def save_metadata(metadata):

    """
    Salva metadata da NF-e no DynamoDB.
    """


    item = convert_decimal(
        metadata
    )


    # garante campos mínimos

    if "chave_acesso" not in item:

        raise Exception(
            "Chave NF-e obrigatória"
        )


    table.put_item(
        Item=item
    )


    return True