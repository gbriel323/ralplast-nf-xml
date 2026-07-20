from lxml import etree



def validate_xml(xml):

    try:

        root = etree.fromstring(
            xml
        )


        if root is None:

            raise Exception(
                "XML inválido"
            )


        return True


    except Exception as e:

        raise Exception(
            f"Erro XML: {e}"
        )