import xml.etree.ElementTree as ET


def extract_metadata(xml: bytes) -> dict:

    try:

        root = ET.fromstring(
            xml
        )


        ns = {
            "nfe": "http://www.portalfiscal.inf.br/nfe"
        }


        chave = root.find(
            ".//nfe:chNFe",
            ns
        )


        # Caso XML não tenha chNFe,
        # tenta buscar pelo atributo Id da infNFe
        if chave is None:

            inf_nfe = root.find(
                ".//nfe:infNFe",
                ns
            )

            if inf_nfe is not None:

                chave_id = inf_nfe.attrib.get(
                    "Id"
                )

                if chave_id:

                    chave_valor = chave_id.replace(
                        "NFe",
                        ""
                    )

                else:

                    chave_valor = None

            else:

                chave_valor = None

        else:

            chave_valor = chave.text



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
                chave_valor,


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
                else 0.0,


            "emitente":
                emitente.text
                if emitente is not None
                else None

        }



    except ET.ParseError as e:

        raise Exception(
            f"XML NF-e inválido: {str(e)}"
        )


    except Exception as e:

        raise Exception(
            f"Erro extraindo metadata NF-e: {str(e)}"
        )