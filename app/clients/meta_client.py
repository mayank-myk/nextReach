import datetime
import hashlib

import requests

META_API_URL = "https://graph.facebook.com/v16.0/{pixel_id}/events"
META_PIXEL_ID = 612504087921019
META_ACCESS_TOKEN = "EAAdUDeSjEqsBO5IIYnQQi7r7v30xJE9Xy4iWVjMrv2tRwiKSBFZBjOASF6u6jE7Qne23bg4ynOrLqmevbiK3GMr7AdOnqrrQm8x9Cqdz1P9q6f1ATyIID8PtXVGCGVWCppjZBaJaGTd96WxgG7ZAGopWR72WU4nxjjwJNETVs838xbgVkbzHgVCmqjgDhC9tQZDZD"


class MetaAPIClient:
    def __init__(self):
        self.pixel_id = META_PIXEL_ID
        self.access_token = META_ACCESS_TOKEN
        self.headers = {"Content-Type": "application/json"}

    def hash_data(self, data: str) -> str:
        """Hashes data using SHA-256 for secure transmission."""
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    def send_event(self, event_name: str, data: dict):
        """Sends an event to Meta API."""
        url = META_API_URL.format(pixel_id=self.pixel_id)
        payload = {
            "data": [
                {
                    "event_name": event_name,
                    "event_time": int(datetime.datetime.now().timestamp()),
                    "user_data": {
                        "ph": self.hash_data(data.get("phone")),
                        "em": self.hash_data(data.get("email").strip().lower()) if data.get("email", "") else None,
                        "fn": self.hash_data(data.get("name").strip().lower()) if data.get("name", "") else None,
                        "external_id": data.get("insta_user_id").strip().lower() if data.get("insta_user_id",
                                                                                             "") else None
                    },
                    "custom_data": data.get("custom_data", {}),
                    "event_source_url": data.get("event_source_url", "")
                }
            ],
            "access_token": self.access_token
        }
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code != 200:
            print(f"Meta API Error: {response.status_code} - {response.text}")
        return response.json()
