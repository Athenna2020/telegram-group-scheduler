import os
import random
import textwrap
import requests
from PIL import Image, ImageDraw, ImageFont

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


QUOTES = [
    ("موفقیت پایان راه نیست؛ شکست هم نابودکننده نیست. آنچه اهمیت دارد شجاعت ادامه دادن است.", "وینستون چرچیل"),
    ("زندگی زمانی زیباتر می‌شود که هر روز دلیلی برای لبخند پیدا کنیم.", "چارلی چاپلین"),
    ("بزرگ‌ترین افتخار ما زمین نخوردن نیست، بلکه برخاستن پس از هر زمین خوردن است.", "کنفوسیوس"),
    ("هر صبح فرصتی تازه است برای ساختن روزی بهتر از دیروز.", "الهام‌بخش"),
    ("آرامش از جایی آغاز می‌شود که تصمیم می‌گیری مثبت فکر کنی.", "اندیشه مثبت"),
]

GOOD_NIGHT_QUOTES = [
    ("شب، فرصتی آرام برای سپاسگزاری از امروز و امید به فرداست.", "شب بخیر"),
    ("آرام بخوابید؛ فردا روزی تازه برای شروعی زیباتر است.", "شب بخیر"),
    ("امشب نگرانی‌ها را زمین بگذارید و با قلبی آرام استراحت کنید.", "شب بخیر"),
]

AD_MESSAGE = """
📢 اطلاعیه تبلیغاتی

دوستان عزیز، برای ثبت آگهی، معرفی خدمات، کسب‌وکار، خرید و فروش، آموزش، کاریابی و سایر اطلاعیه‌ها می‌توانید با مدیران گروه هماهنگ کنید.

لطفاً آگهی‌ها را فقط طبق قوانین گروه ارسال فرمایید.

با احترام 🌿
"""

OPEN_CAPTION = """
🌞 صبح بخیر دوستان عزیز

✅ گروه باز شد و ارسال پیام از ساعت 07:00 مجاز است.

امیدوارم امروز برای همه شما روزی سرشار از انرژی، آرامش، موفقیت و خبرهای خوب باشد.

لطفاً گفتگوها را با احترام، نظم و انرژی مثبت ادامه دهید. 🌿
"""

GOOD_NIGHT_CAPTION = """
🌙 شب بخیر دوستان عزیز

امیدوارم روز خوبی را پشت سر گذاشته باشید.

تا ساعت 00:00 گروه باز است و پس از آن ارسال پیام تا ساعت 07:00 صبح غیرفعال می‌شود.

شبی آرام و پر از سلامتی برای همه شما آرزو می‌کنم. ✨
"""

CLOSE_MESSAGE = """
🔒 گروه بسته شد.

ارسال پیام تا ساعت 07:00 صبح غیرفعال است.

شب آرام و پر از سلامتی برای همه شما آرزو می‌کنم. 🌙
"""


def set_permissions(permissions):
    url = f"{BASE_URL}/setChatPermissions"
    data = {
        "chat_id": GROUP_ID,
        "permissions": permissions
    }

    response = requests.post(url, json=data, timeout=30)
    print(response.text)
    response.raise_for_status()


def send_message(text):
    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": GROUP_ID,
        "text": text
    }

    response = requests.post(url, data=data, timeout=30)
    print(response.text)
    response.raise_for_status()


def send_photo(photo_path, caption):
    url = f"{BASE_URL}/sendPhoto"

    with open(photo_path, "rb") as photo:
        files = {"photo": photo}
        data = {
            "chat_id": GROUP_ID,
            "caption": caption
        }

        response = requests.post(url, data=data, files=files, timeout=60)
        print(response.text)
        response.raise_for_status()


def create_graphic_image(text, author, filename, mode="morning"):
    width, height = 1200, 800

    if mode == "morning":
        bg_color = (245, 252, 240)
        accent_color = (38, 160, 90)
        title = "صبح بخیر"
        emoji = "☀️"
    elif mode == "night":
        bg_color = (20, 28, 55)
        accent_color = (255, 210, 90)
        title = "شب بخیر"
        emoji = "🌙"
    else:
        bg_color = (245, 245, 245)
        accent_color = (60, 120, 200)
        title = "پیام امروز"
        emoji = "✨"

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 72)
        text_font = ImageFont.truetype("DejaVuSans.ttf", 42)
        author_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        author_font = ImageFont.load_default()

    draw.rounded_rectangle(
        (60, 60, width - 60, height - 60),
        radius=40,
        outline=accent_color,
        width=6
    )

    draw.text((100, 100), f"{emoji} {title}", fill=accent_color, font=title_font)

    wrapped = textwrap.wrap(text, width=35)
    y = 260

    text_color = (30, 30, 30) if mode != "night" else (245, 245, 245)

    for line in wrapped:
        draw.text((100, y), line, fill=text_color, font=text_font)
        y += 65

    draw.text(
        (100, height - 160),
        f"— {author}",
        fill=accent_color,
        font=author_font
    )

    img.save(filename)


if ACTION == "open":
    set_permissions(OPEN_PERMISSIONS)

    quote, author = random.choice(QUOTES)
    image_path = "morning_quote.png"

    create_graphic_image(
        text=quote,
        author=author,
        filename=image_path,
        mode="morning"
    )

    send_photo(image_path, OPEN_CAPTION)

elif ACTION == "ad":
    send_message(AD_MESSAGE)

elif ACTION == "goodnight":
    quote, author = random.choice(GOOD_NIGHT_QUOTES)
    image_path = "goodnight.png"

    create_graphic_image(
        text=quote,
        author=author,
        filename=image_path,
        mode="night"
    )

    send_photo(image_path, GOOD_NIGHT_CAPTION)

elif ACTION == "close":
    send_message(CLOSE_MESSAGE)
    set_permissions(CLOSE_PERMISSIONS)

else:
    raise Exception(f"Unknown ACTION: {ACTION}")
