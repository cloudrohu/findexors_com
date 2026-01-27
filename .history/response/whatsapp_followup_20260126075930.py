import urllib.parse
import webbrowser

def send_whatsapp(phone, message):
    url = f"https://wa.me/91{phone}?text={urllib.parse.quote(message)}"
    webbrowser.open(url)
