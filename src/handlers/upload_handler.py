import json


from validators.xml_validator import validate_xml

from services.s3_service import save_xml

from services.nfe_service import extract_metadata

from services.dynamodb_service import save_metadata

from shared.multipart import extract_file




def upload(event, context):

    try:


        print("==============================")
        print("EVENT RECEBIDO")
        print(event)
        print("==============================")



        # ==================================
        # 1 - Extrair arquivo multipart
        # ==================================

        file = extract_file(
            event
        )


        filename = file["filename"]


        xml_content = file["content"]



        print("==============================")
        print("ARQUIVO RECEBIDO")
        print(filename)
        print("==============================")


        print(
            xml_content[:300]
        )



        if not xml_content:

            raise Exception(
                "Arquivo vazio"
            )



        # ==================================
        # 2 - Validar XML
        # ==================================

        validate_xml(
            xml_content
        )


        print(
            "XML VALIDADO"
        )



        # ==================================
        # 3 - Extrair Metadata NF-e
        # ==================================

        metadata = extract_metadata(
            xml_content
        )


        print("==============================")
        print("METADATA")
        print(metadata)
        print("==============================")



        if not metadata.get(
            "nfe_id"
        ):

            raise Exception(
                "Chave de acesso NF-e não encontrada"
            )



        # ==================================
        # 4 - Salvar XML S3
        # ==================================

        s3_info = save_xml(
            xml_content,
            metadata["nfe_id"]
        )


        metadata.update({

            "s3_bucket":
                s3_info["bucket"],

            "s3_key":
                s3_info["key"],

            "filename":
                filename

        })



        print(
            "XML SALVO S3"
        )



        # ==================================
        # 5 - Salvar DynamoDB
        # ==================================

        save_metadata(
            metadata
        )


        print(
            "METADATA SALVO DYNAMODB"
        )



        # ==================================
        # 6 - Response
        # ==================================

        return {


            "statusCode": 200,


            "headers": {

                "Content-Type":
                    "application/json",

                "Access-Control-Allow-Origin":
                    "*"

            },


            "body": json.dumps({

                "message":
                    "NF-e processada com sucesso",


                "nfe_id":
                    metadata["nfe_id"],


                "filename":
                    filename,


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