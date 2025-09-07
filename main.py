import os
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client

URL = "https://www.oakhouse.jp/listv2/get?vacancy_date%5B%5D=2&vacancy_date%5B%5D=3&rent_low=&rent_high=&room_size_low=&room_size_high=&lang=eng&mark%5B%5D=&mark%5B%5D=sr&search_mode=mark&with_booster=true&from_page=sr&state_id%5B%5D=13&route=oakhouse&page=1&ecomars_page_name=%E3%82%BD%E3%83%BC%E3%82%B7%E3%83%A3%E3%83%AB%E3%83%AC%E3%82%B8%E3%83%87%E3%83%B3%E3%82%B9%E7%89%A9%E4%BB%B6%E4%B8%80%E8%A6%A7"

MESSAGE = """🚨 La residencia {term} tiene habitaciones libres para tus fechas. ¡CORRE! Entra en este enlace:
https://www.oakhouse.jp/eng/house/tokyo/social-residence?rent_low=&rent_high=&room_size_low=&room_size_high=&vacancy_date%5B%5D=2&vacancy_date%5B%5D=3&mode=do
"""

def main():
    # Leer variable de entorno para habilitar/deshabilitar el scraper
    scraper_enabled = os.environ.get("SCRAPER_ENABLED", "true").lower()  # por defecto 'true'
    if scraper_enabled in ["0", "false", "no"]:
        print("🛑 Scraper desactivado por SCRAPER_ENABLED")
        return

    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")
    # Buscar todos los elementos h3 con la clase c-caset__name y extraer el texto del enlace <a> dentro
    places = []
    for h3 in soup.find_all("h3", class_="c-caset__name"):
        link = h3.find("a")
        if link:
            places.append(link.get_text(strip=True).lower().strip())

    search_term = os.environ["SEARCH_TERM"].lower().strip()
    search_term_display = search_term  # Variable para mostrar en logs

    if search_term in places:
        client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])
        message = client.messages.create(
            from_="whatsapp:+14155238886",  # Número fijo del Sandbox de Twilio
            to=f"whatsapp:{os.environ['WHATSAPP_TO']}",
            body=MESSAGE.format(term=search_term)
        )
        print(f"✅ WhatsApp enviado con SID: {message.sid}")
    else:
        print(f"❌ '{search_term_display}' no está disponible todavía")

if __name__ == "__main__":
    main()