import azure.functions as func
import json

from mcp_docs_compliance.compliance import check_user_config_compliance
from mcp_docs_compliance.extractor import extract_supported_user_config


app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="check-compliance", methods=["POST"])
def check_compliance(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        supported = extract_supported_user_config(
            body["documentation_text"],
            body["vendor"],
            body["version"],
            body.get("source_url"),
        )
        result = check_user_config_compliance(body["actual_config"], supported)
        return func.HttpResponse(json.dumps(result), mimetype="application/json")
    except Exception as exc:
        return func.HttpResponse(json.dumps({"error": str(exc)}), status_code=400, mimetype="application/json")
