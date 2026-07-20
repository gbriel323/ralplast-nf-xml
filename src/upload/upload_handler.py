import json
from flask import Blueprint, request

from .s3_manager import salvar_no_s3

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/xml/upload", methods=["POST"])
def upload():
    arquivos = request.files.getlist("files")
    bucket = "ralplast-xml-452408242851-sa-east-1-an"

    if not arquivos:
        return json.dumps({"erro": "Nenhum arquivo enviado"}), 400

    urls = []

    for arquivo in arquivos:
        validar_extensao(arquivo.filename)
        url = salvar_no_s3(arquivo, bucket)
        urls.append(url)

    return json.dumps({"urls": urls}), 200


def validar_extensao(filename):
    if not filename.endswith(".xml"):
        raise ValueError("Extensão inválida")