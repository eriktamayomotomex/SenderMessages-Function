import azure.functions as func
import requests
import json
import time
import os

# Token de autenticación de WhatsApp API
TOKEN = "EAAM5a7Gh02IBO5ZAhDwJM9ZCcZC6n605bNU3riaRadb5QoP283gpbNxDfXdqrBDgkFW73W2vQ5mXrDhSBxKmKRp2gKDxCD5OTkIL244DLaGrdqxYZBZCltBjSY0qJ3DxGzZA1OncEMaAgQwIXi0iw3WSW6ynUC6XlXMWjefN0iCiP9rZAWCYa7SRPVe0pxNnIfhNL8B8JMrLWEBk0IDi3fhKCuncekZD"
WHATSAPP_URL = "https://graph.facebook.com/v21.0/472115115983663/messages"

# Lista de números a los que se enviarán los mensajes
NUMEROS = ['8186881028', '8124397789', '8126272826', '8122509882']
MENSAJES_POR_MINUTO = 180
LOG_FILE = "registro_envios.json"

def enviar_mensaje(numero):
    """ Envía un mensaje de WhatsApp a un número específico """
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "template",
        "template": {
            "name": "demo_day_acceso",
            "language": {"code": "es_MX"},
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "image",
                            "image": {"link": "https://bdcmotomex.com/Media/TVS-ACCESO-IMAGEN.jpg"}
                        }
                    ]
                }
            ]
        }
    }

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(WHATSAPP_URL, json=payload, headers=headers)
    return response.json()

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function HTTP para enviar mensajes de WhatsApp en lotes de 180 por minuto.
    """
    enviados = []
    
    # Verifica si el archivo de registro existe, si no, créalo
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)

    for i in range(0, len(NUMEROS), MENSAJES_POR_MINUTO):
        lote = NUMEROS[i:i + MENSAJES_POR_MINUTO]

        for numero in lote:
            respuesta = enviar_mensaje(numero)
            enviados.append({"numero": numero, "respuesta": respuesta})

            # Guardar en el archivo de log JSON
            with open(LOG_FILE, "r+", encoding="utf-8") as file:
                registros = json.load(file)
                registros.append({"numero": numero, "respuesta": respuesta})
                file.seek(0)
                json.dump(registros, file, indent=4)

        # Espera 60 segundos antes del siguiente lote
        if i + MENSAJES_POR_MINUTO < len(NUMEROS):
            time.sleep(60)

    return func.HttpResponse(json.dumps({"status": "Proceso completo", "mensajes_enviados": enviados}, indent=4), mimetype="application/json")
