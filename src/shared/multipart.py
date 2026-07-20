import base64

from email.parser import BytesParser
from email.policy import default



def extract_file(event):


    body = event.get(
        "body"
    )


    if not body:

        raise Exception(
            "Body vazio"
        )



    # ============================
    # Decode API Gateway
    # ============================

    if event.get(
        "isBase64Encoded"
    ):

        body_bytes = base64.b64decode(
            body
        )

    else:

        body_bytes = body.encode(
            "utf-8"
        )



    # ============================
    # Headers
    # ============================

    headers = event.get(
        "headers",
        {}
    )


    print("==============================")
    print("HEADERS RECEBIDOS")
    print(headers)
    print("==============================")



    content_type = None


    for key, value in headers.items():

        if key.lower() == "content-type":

            content_type = value

            break



    if not content_type:

        raise Exception(
            "Content-Type multipart não encontrado"
        )



    print(
        "CONTENT TYPE:"
    )

    print(
        content_type
    )



    # ============================
    # Parse multipart
    # ============================

    mime = BytesParser(
        policy=default
    ).parsebytes(

        (
            "Content-Type: "
            + content_type
            + "\r\n\r\n"
        ).encode("utf-8")
        +
        body_bytes

    )



    for part in mime.iter_attachments():


        filename = part.get_filename()


        payload = part.get_payload(
            decode=True
        )


        if filename:


            return {


                "filename":
                    filename,


                "content":
                    payload

            }



    raise Exception(
        "Nenhum arquivo encontrado"
    )