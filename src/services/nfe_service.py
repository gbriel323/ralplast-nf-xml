from lxml import etree



def extract_metadata(xml):


    root = etree.fromstring(
        xml
    )


    ns = {
        "nfe":
        "http://www.portalfiscal.inf.br/nfe"
    }



    chave = root.find(
        ".//nfe:chNFe",
        ns
    )


    numero = root.find(
        ".//nfe:nNF",
        ns
    )


    serie = root.find(
        ".//nfe:serie",
        ns
    )


    valor = root.find(
        ".//nfe:vNF",
        ns
    )


    emitente = root.find(
        ".//nfe:xNome",
        ns
    )



    return {


        "chave_acesso":
            chave.text
            if chave is not None
            else None,


        "numero":
            numero.text
            if numero is not None
            else None,


        "serie":
            serie.text
            if serie is not None
            else None,


        "valor_total":
            float(valor.text)
            if valor is not None
            else 0,


        "emitente":
            emitente.text
            if emitente is not None
            else None

    }