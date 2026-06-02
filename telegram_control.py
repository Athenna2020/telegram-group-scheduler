import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")
ACTION = os.getenv("ACTION")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN is missing")

if not GROUP_ID:
    raise Exception("GROUP_ID is missing")

if not ACTION:
    raise Exception("ACTION is missing")


BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


OPEN_PERMISSIONS = {
    "can_send_messages": True,
    "can_send_audios": True,
    "can_send_documents": True,
    "can_send_photos": True,
    "can_send_videos": True,
    "can_send_video_notes": True,
    "can_send_voice_notes": True,
    "can_send_polls": True,
    "can_send_other_messages": True,
    "can_add_web_page_previews": True,
}

CLOSE_PERMISSIONS = {
    "can_send_messages": False,
    "can_send_audios": False,
    "can_send_documents": False,
    "can_send_photos": False,
    "can_send_videos": False,
    "can_send_video_notes": False,
    "can_send_voice_notes": False,
    "can_send_polls": False,
    "can_send_other_messages": False,
    "can_add_web_page_previews": False,
}


GOOD_MORNING_MESSAGE = """
🌞 صبح بخیر دوستان عزیز

✅ گروه باز شد و ارسال پیام از ساعت 07:00 مجاز است.

امیدوارم امروز برای همه شما روزی سرشار از انرژی، آرامش، موفقیت و خبرهای خوب باشد.

لطفاً گفتگوها را با احترام، نظم و انرژی مثبت ادامه دهید. 🌿
"""

WARNING_MESSAGE = """
⚠️ یادآوری مهم

تا ۱۰ دقیقه دیگر گروه بسته خواهد شد.

⏰ زمان بسته شدن: 00:30 بامداد
🔒 بعد از این زمان امکان ارسال پیام تا ساعت 07:00 صبح غیرفعال می‌شود.

لطفاً اگر پیام مهمی دارید، همین حالا ارسال کنید.
"""

CLOSE_MESSAGE = """
🔒 گروه بسته شد.

ارسال پیام تا ساعت 07:00 صبح غیرفعال است.

شب آرام و پر از سلامتی برای همه شما آرزو می‌کنم. 🌙
"""


def send_message(text):
    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": GROUP_ID,
        "text": text
    }

    response = requests.post(url, data=data, timeout=30)
    print(response.text)
    response.raise_for_status()


def set_permissions(permissions):
    url = f"{BASE_URL}/setChatPermissions"
    data = {
        "chat_id": GROUP_ID,
        "permissions": permissions
    }

    response = requests.post(url, json=data, timeout=30)
    print(response.text)
    response.raise_for_status()


if ACTION == "open":
    set_permissions(OPEN_PERMISSIONS)
    send_message(GOOD_MORNING_MESSAGE)

elif ACTION == "warning":
    send_message(WARNING_MESSAGE)

elif ACTION == "close":
    send_message(CLOSE_MESSAGE)
    set_permissions(CLOSE_PERMISSIONS)

else:
    raise Exception(f"Unknown ACTION: {ACTION}")
