import os
import requests

OCR_SPACE_KEY = os.getenv("OCR_SPACE_KEY", "helloworld")  # Use your own key for production

def fetch_and_extract(url, session_id: str):
    # Download the image with proper session cookie
    resp = requests.get(url, cookies={"ASP.NET_SessionId": session_id})
    resp.raise_for_status()

    # Prepare file payload with a suggested filename to set content type
    files = {
        "file": ("captcha.png", resp.content, "image/png")
    }

    data = {
        "apikey": OCR_SPACE_KEY,
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
        print(response.text)

        print(self.session_id)

if __name__ == "__main__":
    client = AuthClient()