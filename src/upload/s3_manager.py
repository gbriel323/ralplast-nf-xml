import boto3

def salvar_no_s3(arquivo, bucket):
    s3 = boto3.client('s3')
    s3.upload_fileobj(arquivo, bucket, arquivo.filename)  # Usa upload_fileobj para objetos de arquivo
    return f"s3://{bucket}/{arquivo.filename}"
