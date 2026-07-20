def validar_xml(xml):

    if xml is None:
        raise Exception("XML não informado.")

    if len(xml) == 0:
        raise Exception("Arquivo vazio.")