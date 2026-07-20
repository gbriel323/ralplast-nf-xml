from lxml import etree



NFE_NAMESPACE = {
    "nfe": "http://www.portalfiscal.inf.br/nfe"
}



def extract_metadata(xml):


    root = etree.fromstring(
        xml
    )



    # ===============================
    # Chave NF-e
    # ===============================

    chave = root.find(
        ".//nfe:protNFe/nfe:infProt/nfe:chNFe",
        namespaces=NFE_NAMESPACE
    )


    # fallback pelo Id da infNFe
    if chave is None:


        inf_nfe = root.find(
            ".//nfe:infNFe",
            namespaces=NFE_NAMESPACE
        )


        if inf_nfe is not None:


            nfe_id = inf_nfe.get(
                "Id"
            )


            if nfe_id:

                chave = nfe_id.replace(
                    "NFe",
                    ""
                )



    # ===============================
    # Dados básicos
    # ===============================


    numero = root.find(
        ".//nfe:ide/nfe:nNF",
        namespaces=NFE_NAMESPACE
    )


    serie = root.find(
        ".//nfe:ide/nfe:serie",
        namespaces=NFE_NAMESPACE
    )


    valor = root.find(
        ".//nfe:ICMSTot/nfe:vNF",
        namespaces=NFE_NAMESPACE
    )


    emitente = root.find(
        ".//nfe:emit/nfe:xNome",
        namespaces=NFE_NAMESPACE
    )



    return {


        "chave_acesso":

            chave.text.strip()
            if hasattr(chave, "text")
            else chave,



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