# send_sms.py (Textbelt version)
import requests
import random

# Free daily test key: 'textbelt'
TEXTBELT_API_KEY = 'textbelt'

# Sample motivational quotes
QUOTES = [
    "Every day is a step toward healing. 🌿",
    "Let nature work its magic — stay strong! 🌞",
    "You’re doing amazing. Keep going. 💚",
    "Ayurveda is patience in action. 🌼",
    "Small efforts, big results over time. ✨"
]

def build_reminder_message(medicine):
    quote = random.choice(QUOTES)
    return f"""
AyurBot Reminder 🌿

💊 Remedy: {medicine['medicine']}
🕒 Dose: {medicine['dose']}
📌 Motivation: {quote}
"""

def send_remedy_sms(to_number, medicine):
    message = build_reminder_message(medicine)

    res = requests.post('https://textbelt.com/text', {
        'phone': to_number,
        'message': message,
        'key': TEXTBELT_API_KEY
    })

    result = res.json()
    if result.get('success'):
        return "✅ SMS sent successfully via Textbelt!"
    else:
        return f"❌ SMS failed: {result.get('error', 'Unknown error')}"
