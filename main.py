# main.py

from datetime import datetime
import os, json, requests
from auth import AuthClient
from automator import FunTargetAPIClient
from appwrite.client import Client
from appwrite.services.storage import Storage
from appwrite.input_file import InputFile


import easyocr




# Initialize Appwrite SDK
client = Client()
client.set_endpoint(os.getenv("APPWRITE_FUNCTION_ENDPOINT"))
client.set_project(os.getenv("APPWRITE_FUNCTION_PROJECT_ID"))
client.set_key(os.getenv("APPWRITE_FUNCTION_API_KEY"))  # key provided automatically
storage = Storage(client)

def main(req, res):
    # Your existing data-fetch logic
    authclient = AuthClient()
    session_id = authclient.get_session_id()
    fun_client = FunTargetAPIClient(session_id)

    data = {
        "fun_target": fun_client.get_fun_target_data(),
        "fun_roullet": fun_client.get_fun_roullet_data(),
        "triple_fun": fun_client.get_triple_fun_data(),
        "fun_ab": fun_client.get_fun_ab_data()
    }

    now = datetime.now().strftime("%Y%m%dT%H%M%SZ")
    bucket_id = os.getenv("BUCKET_ID")
    uploaded = []

    print(data["fun_ab"])

    for key, value in data.items():
        json_bytes = json.dumps(value, indent=4).encode("utf-8")
        file_id = f"{key}_{now}.json"
        result = storage.create_file(
            bucket_id=bucket_id,
            file_id=file_id,
            file=InputFile.from_bytes(json_bytes, file_id, content_type="application/json"),
            permissions=["read(any)"]
        )
        uploaded.append(result["$id"])
        res.log(f"Uploaded {file_id} -> {result['$id']}")

    return res.json({"status": "success", "uploaded": uploaded})


