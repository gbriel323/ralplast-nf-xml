import json
import base64

from validators.xml_validator import validate_xml

from services.s3_service import save_xml

from services.nfe_service import extract_metadata

from services.dynamodb_service import save_metadata


def upload(event, context):

    try:

        # ===============================
        # 1 - Receber XML
        # ===============================

        body = event.get("body")


        if not body:
            raise Exception(
                "XML não informado"
            )


        if event.get("isBase64Encoded"):

            xml_content = base64.b64decode(
                body
            )

        else:

            xml_content = body.encode(
                "utf-8"
            )


        # ===============================
        # 2 - Validar XML
        # ===============================

        validate_xml(
            xml_content
        )


        # ===============================
        # 3 - Extrair dados NF-e
        # ===============================

        metadata = extract_metadata(
            xml_content
        )


        if not metadata.get("chave_acesso"):

            raise Exception(
                "Chave de acesso NF-e não encontrada"
            )


        # ===============================
        # 4 - Salvar XML no S3
        # ===============================

        s3_info = save_xml(
            xml_content
        )


        metadata.update({

            "s3_bucket":
                s3_info["bucket"],

            "s3_key":
                s3_info["key"]

        })


        # ===============================
        # 5 - Salvar Metadata DynamoDB
        # ===============================

        save_metadata(
            metadata
        )


        # ===============================
        # 6 - Retorno
        # ===============================

        return {

            "statusCode": 200,

            "headers": {
                "Content-Type": "application/json"
            },

            "body": json.dumps({

                "message":
                    "NF-e processada com sucesso",

                "nfe_id":
                    metadata["chave_acesso"],

                "s3_key":
                    s3_info["key"]

            })

        }


    except Exception as e:


        print(
            f"Erro processamento NF-e: {str(e)}"
        )


        return {

            "statusCode": 500,

            "headers": {
                "Content-Type": "application/json"
            },

            "body": json.dumps({

                "error":
                    str(e)

            })

        }