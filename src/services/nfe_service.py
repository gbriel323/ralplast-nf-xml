import xml.etree.ElementTree as ET



def remove_namespace(tag):

    return tag.split("}")[-1]



def find_element(root, name):

    for element in root.iter():

        if remove_namespace(element.tag) == name:

            return element

    return None



def extract_metadata(xml):


    root = ET.fromstring(
        xml
    )


    # ===============================
    # Chave NF-e
    # ===============================

    chave = find_element(
        root,
        "chNFe"
    )


    chave_acesso = None


    if chave is not None:

        chave_acesso = chave.text.strip()



    # fallback pelo Id da infNFe

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



    # ===============================
    # Campos NF-e
    # ===============================

    numero = find_element(
        root,
        "nNF"
    )


    serie = find_element(
        root,
        "serie"
    )


    valor = find_element(
        root,
        "vNF"
    )


    emitente = find_element(
        root,
        "xNome"
    )



    return {


        "chave_acesso":

            chave_acesso,



        "numero":

            numero.text.strip()
            if numero is not None
            else None,



        "serie":

            serie.text.strip()
            if serie is not None
            else None,



        "valor_total":

            float(valor.text)
            if valor is not None
            else 0,



        "emitente":

            emitente.text.strip()
            if emitente is not None
            else None

    }