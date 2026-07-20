import json


def success(data):

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "success": True,
            "data": data
        })
    }


def error(message):

    return {
        "statusCode": 400,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "success": False,
            "message": message
        })
    }