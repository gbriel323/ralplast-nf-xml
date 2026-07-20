import base64

from services.s3_service import salvar_no_s3
from validators.xml_validator import validar_xml
from shared.response import success, error


def process_upload(event):

    try:

        body = event.get("body")

        if event.get("isBase64Encoded"):
            body = base64.b64decode(body)

        validar_xml(body)

        resultado = salvar_no_s3(body)

        return success(resultado)

    except Exception as ex:

        return error(str(ex))