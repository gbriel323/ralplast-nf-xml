import xml.etree.ElementTree as ET


def validate_xml(xml: bytes):

    try:

        root = ET.fromstring(
            xml
        )


        if root is None:

            raise Exception(
                "XML inválido"
            )


        return True


    except ET.ParseError as e:

        raise Exception(
            f"XML inválido: {str(e)}"
        )


    except Exception as e:

        raise Exception(
            f"Erro XML: {str(e)}"
        )