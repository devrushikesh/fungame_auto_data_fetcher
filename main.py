# main.py

from datetime import datetime
import os, json, requests
from termcolor import colored
import boto3


class AuthClient:

    def __init__(self):
        
        self.session = requests.Session()
        self.get_initial_session_id()



    def get_initial_session_id(self):


        url = "https://www.playrep.pro/Login.mvc"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Referer": "https://www.playrep.pro/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9",
            "Upgrade-Insecure-Requests": "1"
        }


        response = self.session.get(url, headers=headers)
        # Extract the session ID from cookies
        self.session_id = self.session.cookies.get("ASP.NET_SessionId")
        print(self.session_id)

        self.get_captcha()
    

    def get_captcha(self):
        # URLs for the captchas
        url1 = "https://www.playrep.pro/Login.mvc/CaptchaImage"
        url2 = "https://www.playrep.pro/Login.mvc/CaptchaImage2"

        # Extract each captcha
        digits1 = fetch_and_extract(url1, session_id=self.session_id)
        digits2 = fetch_and_extract(url2, session_id=self.session_id)

        # Concatenate
        self.captcha_result = digits1 + digits2
        print("Result:", self.captcha_result)

        self.login()

    def get_session_id(self):
        return self.session_id

    def login(self):
        payload = {
            "strLoginID": "GK00106030",
            "strLoginPassword": "LYCXKATJ",
            "strCaptcha": self.captcha_result,
            "btnCheckLogin": "Login"
        }

        self.session.headers.update({
            "Host": "www.playrep.pro",
            "Cookie": f"ASP.NET_SessionId={self.session_id}",
            "Cache-Control": "max-age=0",
            "Sec-Ch-Ua": '"Chromium";v="137", "Not/A)Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://www.playrep.pro",
            "Content-Type": "application/x-www-form-urlencoded",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"),
            "Accept": ("text/html,application/xhtml+xml,application/xml;q=0.9,"
                    "image/avif,image/webp,image/apng,*/*;q=0.8,"
                    "application/signed-exchange;v=b3;q=0.7"),
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://www.playrep.pro/",
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=0, i"
        })

        response = self.session.post("https://www.playrep.pro/Login.mvc", data=payload)

        print("Status code:", response.status_code)


class FunTargetAPIClient:
    BASE_URL = "https://playrep.pro"
    
    def __init__(self, session_id):
        print("now we are in fun target api client")
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
        print(f"🔧 Making API request to {url}")
        try:
            resp = self.session.post(url, json={})
            print("→ HTTP status:", resp.status_code)
            
            # Check for non-OK status
            if resp.status_code != 200:
                print("⚠️ Unexpected status code:", resp.text)
                resp.raise_for_status()
            
            # Check content type
            ctype = resp.headers.get("Content-Type", "")
            print("→ Content-Type:", ctype)
            
            # Safe JSON parse
            try:
                return resp.json()
            except ValueError as ve:
                print("💥 JSON parse error, response text:", resp.text[:200])
                raise
            
        except Exception as ex:
            print("❌ Error while fetching data:", ex)
            raise

    def get_fun_target_data(self):
        return self._post("/DrawDetails.mvc/FunTargetData")

    def get_fun_roullet_data(self):
        return self._post("/DrawDetails.mvc/FunRoulletData")

    def get_triple_fun_data(self):
        return self._post("/DrawDetails.mvc/TripleFunData")

    def get_fun_ab_data(self):
        return self._post("/DrawDetails.mvc/FunABData")


def fetch_and_extract(url, session_id: str):
    print("called fetch and extract captcha")
    # Download the image with proper session cookie
    resp = requests.get(url, cookies={"ASP.NET_SessionId": session_id})
    resp.raise_for_status()


    # Prepare file payload with a suggested filename to set content type
    files = {
        "file": ("captcha.png", resp.content, "image/png")
    }

    data = {
        "apikey": "K87096451388957",
        "language": "eng",
        "isOverlayRequired": False,
        "detectOrientation": True,
        "scale": True,
        "OCREngine": 2  # Better for numeric captcha accuracy
    }

    api_resp = requests.post("https://api.ocr.space/parse/image", files=files, data=data)
    api_resp.raise_for_status()
    result = api_resp.json()

    if result.get("IsErroredOnProcessing"):
        raise RuntimeError(result.get("ErrorMessage", "OCR.space error"))

    text = result["ParsedResults"][0]["ParsedText"]
    digits = ''.join(ch for ch in text if ch.isdigit())

    print(f"OCR '{url}' → {digits}")
    return digits

def lambda_handler(event, context):
    try:
        # Init S3 client
        s3 = boto3.client('s3')
        bucket_name = "fungame-lambda-data-bucket"  # 🔁 Replace with your actual S3 bucket name

        # Current timestamp
        now = datetime.now().strftime("%Y%m%dT%H%M%SZ")

        # Auth & Session
        auth = AuthClient()
        sid = auth.get_session_id()
        fun = FunTargetAPIClient(sid)

        # Prepare data
        files = {
            "funtarget": fun.get_fun_target_data(),
            "funab": fun.get_fun_ab_data(),
            "funtriple": fun.get_triple_fun_data(),
            "funrollet": fun.get_fun_roullet_data()
        }

        # Upload each data as JSON to S3
        for folder, data in files.items():
            key = f"{folder}/{now}.json"
            print(f"Uploading {key}...")
            s3.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=json.dumps(data),
                ContentType="application/json"
            )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "All files uploaded successfully",
                "timestamp": now,
                "uploaded_keys": list(files.keys())
            })
        }

    except Exception as e:
        print("❌ Error in Lambda execution:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
