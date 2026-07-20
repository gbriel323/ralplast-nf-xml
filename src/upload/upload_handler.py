import json
from flask import Flask, request
from .s3_manager import salvar_no_s3
from ..utils import registrar_importacao

app = Flask(__name__)

@app.route('/xml/upload', methods=['POST'])
def upload():
    arquivos = request.files.getlist('files')  # Aceitar múltiplos arquivos
    bucket = "ralplast-xml-452408242851-sa-east-1-an"  # Nome do seu bucket S3

    urls = []
    for arquivo in arquivos:
        # Validar a extensão
        try:
            validar_extensao(arquivo.filename)
        except ValueError as e:
            return str(e), 400

        # Salvar no S3 e registrar importação
        url = salvar_no_s3(arquivo, bucket)
        registrar_importacao(arquivo.filename, "usuario_exemplo")  # Substitua pelo usuário real
        urls.append(url)

    return json.dumps({"urls": urls}), 200

def validar_extensao(arquivo):
    if not arquivo.filename.endswith('.xml'):
        raise ValueError("Extensão inválida: apenas arquivos .xml são suportados")
