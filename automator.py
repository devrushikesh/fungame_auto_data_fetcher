import requests
from datetime import datetime
import os
import json

class FunTargetAPIClient:
    BASE_URL = "https://playrep.pro"
    
    def __init__(self, session_id):
        self.session = requests.Session()
        self.session.headers.update({
            "Host": "playrep.pro",
            "Cookie": f"ASP.NET_SessionId={session_id}",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Ch-Ua": '"Chromium";v="135", "Not-A.Brand";v="8"',
            "Sec-Ch-Ua-Mobile": "?0",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/json; charset=UTF-8",
            "Origin": "https://playrep.pro",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=1, i"
        })

    def _post(self, endpoint: str):
        url = f"{self.BASE_URL}{endpoint}"
        referer_url = f"{self.BASE_URL}{endpoint.replace('Data', '')}"
        self.session.headers.update({"Referer": referer_url})
        response = self.session.post(url, json={})
        response.raise_for_status()
        return response.json()

    def get_fun_target_data(self):
        return self._post("/DrawDetails.mvc/FunTargetData")

    def get_fun_roullet_data(self):
        return self._post("/DrawDetails.mvc/FunRoulletData")

    def get_triple_fun_data(self):
        return self._post("/DrawDetails.mvc/TripleFunData")

    def get_fun_ab_data(self):
        return self._post("/DrawDetails.mvc/FunABData")


if __name__ == "__main__":
    session_id = "yoigmtkgik1o3tcle5x3fph4"  # Replace with actual session ID
    client = FunTargetAPIClient(session_id)

    try:
        data = {
            "fun_target": client.get_fun_target_data(),
            "fun_roullet": client.get_fun_roullet_data(),
            "triple_fun": client.get_triple_fun_data(),
            "fun_ab": client.get_fun_ab_data()
        }
        print(data["fun_ab"])

        os.makedirs("data", exist_ok=True)
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        for k, v in data.items():
            with open(f"./data/output_{k}_{now}.txt", "w", encoding="utf-8") as file:
                file.write(json.dumps(v, indent=4))  # 👈 Write clean JSON string to .txt

        print("✅ Data saved as plain text files.")

    except requests.HTTPError as e:
        print("❌ HTTP Error:", e)

    except Exception as e:
        print("❌ General Error:", e)
