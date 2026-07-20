from email.parser import BytesParser
from email.policy import default


def extract_file(event):

    body = event["body"]


    if event.get("isBase64Encoded"):

        body = body.encode("utf-8")


        import base64

        body = base64.b64decode(body)

    else:

        body = body.encode("utf-8")


    content_type = (
        event["headers"].get("content-type")
        or event["headers"].get("Content-Type")
    )


    message = BytesParser(
        policy=default
    ).parsebytes(

        b"Content-Type: "
        + content_type.encode()
        + b"\r\n\r\n"
        + body

    )


    for part in message.iter_attachments():

        filename = part.get_filename()

        payload = part.get_payload(decode=True)

        return filename, payload


    raise Exception(
        "Arquivo XML não encontrado."
    )