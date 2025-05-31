import requests
import json

def load_lottieurl(url: str):
    try:
        if url.startswith("http"):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        else:
            with open(url, "r") as f:
                return json.load(f)
    except:
        return None