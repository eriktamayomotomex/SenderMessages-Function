import azure.functions as func
import logging
from whatsapp_function import main as whatsapp_main  # Importamos la función de WhatsApp

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="enviar_mensajes")
def enviar_mensajes(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Iniciando el envío de mensajes de WhatsApp.')
    return whatsapp_main(req)  # Llama a la función principal
