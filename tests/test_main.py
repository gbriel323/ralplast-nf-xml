import subprocess
import json

def test_lambda_handler():
    # Simular um evento e contexto de entrada
    event = {}
    context = {}
    
    # Chamar a função lambda_handler
    from src.main import lambda_handler
    response = lambda_handler(event, context)

    # Verifique se a resposta está correta
    assert response['statusCode'] == 200
    assert json.loads(response['body']) == 'Hello from Lambda do Gabriel !'
