import urllib.parse

def send_whatsapp_welcome(response):
    name = response.contact_persone or "Sir/Madam"

    message = f"""
Hello 👋 {name}

✅ We have received your response from our online advertisement.

Thank you for contacting Google Findexor 🚀

Please reply with:
1️⃣ Business Type
2️⃣ City
3️⃣ Requirement (Website / Ads / Both)

Our team will contact you shortly.
"""

    encoded = urllib.parse.quote(message)
    phone = response.contact_no

    whatsapp_url = f"https://wa.me/91{phone}?text={encoded}"

    # 👉 yahan sirf log / future API
    print("WhatsApp URL:", whatsapp_url)
