from handlers.upload_handler import upload


def lambda_handler(event, context):
    return upload(event, context)