import azure.functions as func
from src.transform import transform_data

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = transform_data()
        return func.JsonResponse(data)
    except Exception as e:
        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=500
        )