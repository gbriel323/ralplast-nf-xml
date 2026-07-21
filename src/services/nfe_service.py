import xml.etree.ElementTree as ET



def remove_namespace(tag):

    """
    Remove namespace do XML.

    Ex:
    {http://www.portalfiscal.inf.br/nfe}nNF

    vira:

    nNF
    """

    return tag.split("}")[-1]



def find_element(root, name):

    """
    Busca elemento independente de namespace.
    """

    for element in root.iter():

        if remove_namespace(element.tag) == name:

            return element

    return None



def get_text(element):

    """
    Retorna texto tratado do XML.
    """

    if element is not None and element.text:

        return element.text.strip()

    return None



def extract_metadata(xml):

    """
    Extrai informações básicas da NF-e.
    """

    root = ET.fromstring(
        xml
    )


    # ==================================
    # Chave NF-e
    # ==================================

    chave = find_element(
        root,
        "chNFe"
    )


    chave_acesso = get_text(
        chave
    )


    # Caso não exista no protocolo,
    # pega pelo Id da infNFe

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



    return {


        "chave_acesso":

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