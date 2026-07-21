import xml.etree.ElementTree as ET


def remove_namespace(tag):

    """
    Remove o namespace do XML.

    Exemplo:

    {http://www.portalfiscal.inf.br/nfe}nNF

    Resultado:

    nNF
    """

    return tag.split("}")[-1]


def find_element(root, name):

    """
    Busca um elemento pelo nome,
    independente do namespace.
    """

    for element in root.iter():

        if remove_namespace(element.tag) == name:

            return element

    return None


def get_text(element):

    """
    Retorna o texto tratado de um elemento XML.
    """

    if element is not None and element.text:

        return element.text.strip()

    return None


def extract_metadata(xml):

    """
    Extrai os principais metadados da NF-e.
    """

    root = ET.fromstring(
        xml
    )


    # ==================================
    # Chave de acesso NF-e
    # ==================================

    chave = find_element(
        root,
        "chNFe"
    )


    chave_acesso = get_text(
        chave
    )


    # ==================================
    # Fallback pelo Id da infNFe
    # ==================================

    if not chave_acesso:

        inf_nfe = find_element(
            root,
            "infNFe"
        )


        if inf_nfe is not None:

            nfe_id = inf_nfe.attrib.get(
                "Id"
            )


            if nfe_id:

                chave_acesso = nfe_id.replace(
                    "NFe",
                    ""
                )


    # ==================================
    # Validar chave
    # ==================================

    if not chave_acesso:

        raise Exception(
            "Chave de acesso NF-e não encontrada"
        )


    # ==================================
    # Número NF
    # ==================================

    numero = find_element(
        root,
        "nNF"
    )


    # ==================================
    # Série
    # ==================================

    serie = find_element(
        root,
        "serie"
    )


    # ==================================
    # Valor total
    # ==================================

    valor = find_element(
        root,
        "vNF"
    )


    valor_total = 0


    if valor is not None and valor.text:

        valor_total = float(
            valor.text.strip()
        )


    # ==================================
    # Emitente
    # ==================================

    emitente = find_element(
        root,
        "xNome"
    )


    # ==================================
    # Retorno
    # ==================================

    return {

        "nfe_id":
            chave_acesso,

        "numero":
            get_text(
                numero
            ),

        "serie":
            get_text(
                serie
            ),

        "valor_total":
            valor_total,

        "emitente":
            get_text(
                emitente
            )

    }