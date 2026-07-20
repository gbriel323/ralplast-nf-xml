import xml.etree.ElementTree as ET



NFE_NAMESPACE = {
    "nfe": "http://www.portalfiscal.inf.br/nfe"
}



def extract_metadata(xml):

    root = ET.fromstring(
        xml
    )


    # ===============================
    # Chave NF-e
    # ===============================

    chave = root.find(
        ".//nfe:protNFe/nfe:infProt/nfe:chNFe",
        NFE_NAMESPACE
    )


    chave_acesso = None


    if chave is not None:

        chave_acesso = chave.text.strip()



    # fallback usando Id da infNFe

    if not chave_acesso:


        inf_nfe = root.find(
            ".//nfe:infNFe",
            NFE_NAMESPACE
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
    # Dados NF-e
    # ===============================


    numero = root.find(
        ".//nfe:ide/nfe:nNF",
        NFE_NAMESPACE
    )


    serie = root.find(
        ".//nfe:ide/nfe:serie",
        NFE_NAMESPACE
    )


    valor = root.find(
        ".//nfe:ICMSTot/nfe:vNF",
        NFE_NAMESPACE
    )


    emitente = root.find(
        ".//nfe:emit/nfe:xNome",
        NFE_NAMESPACE
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

            float(valor.text.strip())
            if valor is not None
            else 0,



        "emitente":

            emitente.text.strip()
            if emitente is not None
            else None

    }