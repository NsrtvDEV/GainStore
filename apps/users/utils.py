import requests
from django.conf import settings

BASE_URL = "https://devsms.uz/api"

headers = {
    "Authorization": f"Bearer {settings.DEVSMS_TOKEN}",
    "Content-Type": "application/json",
}


def send_sms(phone: str, message: str) -> dict:
    response = requests.post(
        f"{BASE_URL}/send_sms.php",
        headers=headers,
        json={"phone": phone, "message": message},
    )
    return response.json()


def generate_code():
    import random

    d1 = random.randint(0, 9)
    d2 = random.randint(0, 9)
    d3 = random.randint(0, 9)
    d4 = random.randint(0, 9)
    d5 = random.randint(0, 9)
    d6 = random.randint(0, 9)

    return f"{d1}{d2}{d3}{d4}{d5}{d6}"


def get_balance() -> dict:
    """Проверка баланса DevSMS — можно вызвать из /admin/balance"""
    headers = {
        "Authorization": f"Bearer {settings.DEVSMS_TOKEN}",
        "Content-Type": "application/json",
    }

    response = requests.get(
        f"{BASE_URL}/get_balance.php",
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
