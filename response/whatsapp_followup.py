import urllib.parse
import webbrowser


def send_whatsapp(phone, message):
    """
    Click-to-WhatsApp sender
    (Browser open karega – API ke bina best possible way)
    """
    if not phone or not message:
        return

    phone = str(phone).strip()
    encoded_message = urllib.parse.quote(message)

    url = f"https://wa.me/91{phone}?text={encoded_message}"

    # Open WhatsApp in browser
    webbrowser.open(url)
