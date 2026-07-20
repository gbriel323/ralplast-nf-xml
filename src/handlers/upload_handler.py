import json
import base64

from validators.xml_validator import validate_xml

from services.s3_service import save_xml

from services.nfe_service import extract_metadata

from services.dynamodb_service import save_metadata


def upload_handler(event, context):

    try:

        body = event.get("body")


        if event.get("isBase64Encoded"):

            xml_content = base64.b64decode(body)

        else:

            xml_content = body.encode()



        # 1 - Validar XML

        validate_xml(
            xml_content
        )



        # 2 - Extrair dados NF-e

        metadata = extract_metadata(
            xml_content
        )



        # 3 - Salvar XML

        s3_path = save_xml(
            xml_content,
            metadata["chave_acesso"]
        )



        # 4 - Salvar metadata

        metadata["s3_path"] = s3_path


        save_metadata(
            metadata
        )



        return {

            "statusCode": 200,

            "body": json.dumps({

                "message":
                "NF-e processada",

                "id":
                metadata["chave_acesso"]

            })

        }


    except Exception as e:


        return {

            "statusCode":500,

            "body":json.dumps({

                "error":str(e)

            })

        }