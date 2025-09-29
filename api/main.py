import azure.functions as func
import json 
from src.transform import transform_data

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = transform_data()
        json_data = json.dumps(data, ensure_ascii=False)  # ✅ Convert to JSON string
        return func.HttpResponse(
            body=json_data,
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=500
        )