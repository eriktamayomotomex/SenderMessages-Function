import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="enviar_mensajes")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hola, {name}. La función se ejecutó correctamente.")
    else:
        return func.HttpResponse(
            "La función se ejecutó correctamente. Envia un parámetro 'name' para personalizar la respuesta.",
            status_code=200
        )
