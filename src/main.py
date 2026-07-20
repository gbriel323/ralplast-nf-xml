from handlers.upload_handler import upload


def handler(event, context):
    return upload(event)