import json
import base64


from validators.xml_validator import validate_xml

from services.s3_service import save_xml

from services.nfe_service import extract_metadata

from services.dynamodb_service import save_metadata



def upload(event, context):

    try:


        # ==================================
        # DEBUG API GATEWAY
        # ==================================

        print("==============================")
        print("EVENT RECEBIDO")
        print(event)
        print("==============================")


        # ==================================
        # 1 - Receber XML
        # ==================================

        body = event.get(
            "body"
        )


        print("==============================")
        print("BODY RECEBIDO")
        print(body)
        print("==============================")


        if not body:

            raise Exception(
                "XML não informado"
            )



        # ==================================
        # 2 - Converter XML
        # ==================================

        if event.get(
            "isBase64Encoded"
        ):


            print(
                "Body em Base64"
            )


            xml_content = base64.b64decode(
                body
            )


        else:


            xml_content = body.strip().encode(
                "utf-8"
            )



        print("==============================")
        print("XML RECEBIDO")
        print(xml_content[:300])
        print("==============================")



        # ==================================
        # 3 - Validar XML
        # ==================================

        validate_xml(
            xml_content
        )


        print(
            "XML VALIDADO"
        )



        # ==================================
        # 4 - Extrair Metadata NF-e
        # ==================================

        metadata = extract_metadata(
            xml_content
        )


        print("==============================")
        print("METADATA")
        print(metadata)
        print("==============================")



        if not metadata.get(
            "chave_acesso"
        ):

            raise Exception(
                "Chave de acesso NF-e não encontrada"
            )



        # ==================================
        # 5 - Salvar XML S3
        # ==================================

        s3_info = save_xml(
            xml_content
        )


        metadata.update({

            "s3_bucket":
                s3_info["bucket"],

            "s3_key":
                s3_info["key"]

        })


        print(
            "XML SALVO S3"
        )



        # ==================================
        # 6 - Salvar DynamoDB
        # ==================================

        save_metadata(
            metadata
        )


        print(
            "METADATA SALVO DYNAMODB"
        )



        # ==================================
        # 7 - Response
        # ==================================

        return {


            "statusCode": 200,


            "headers": {

                "Content-Type":
                    "application/json",

                "Access-Control-Allow-Origin":
                    "*",

                "Access-Control-Allow-Headers":
                    "Content-Type,Authorization",

                "Access-Control-Allow-Methods":
                    "OPTIONS,POST"

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


        print("==============================")
        print("ERRO PROCESSAMENTO NF-e")
        print(str(e))
        print("==============================")


        return {


            "statusCode": 500,


            "headers": {

                "Content-Type":
                    "application/json",

                "Access-Control-Allow-Origin":
                    "*"

            },


            "body": json.dumps({

                "error":
                    str(e)

            })

        }