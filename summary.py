import os
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client

URL = "https://www.oakhouse.jp/listv2/get?vacancy_date%5B%5D=2&vacancy_date%5B%5D=3&rent_low=&rent_high=&room_size_low=&room_size_high=&lang=eng&mark%5B%5D=&mark%5B%5D=sr&search_mode=mark&with_booster=true&from_page=sr&state_id%5B%5D=13&route=oakhouse&page=1&ecomars_page_name=%E3%82%BD%E3%83%BC%E3%82%B7%E3%83%A3%E3%83%AB%E3%83%AC%E3%82%B8%E3%83%87%E3%83%B3%E3%82%B9%E7%89%A9%E4%BB%B6%E4%B8%80%E8%A6%A7"

def main():
    """Daily summary que envía por WhatsApp el listado de residencias disponibles"""
    
    try:
        # Hacer la petición a la página
        print("🔍 Obteniendo datos de Oakhouse...")
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Buscar todos los elementos h3 con la clase c-caset__name y extraer el texto del enlace <a> dentro
        places = []
        for h3 in soup.find_all("h3", class_="c-caset__name"):
            link = h3.find("a")
            if link:
                places.append(link.get_text(strip=True))
        
        # Crear mensaje con el listado
        if places:
            message_body = f"""🏠 LISTADO DE RESIDENCIAS DISPONIBLES - Oakhouse

📊 Total de residencias encontradas: {len(places)}

📋 Listado completo:
"""
            for i, place in enumerate(places, 1):
                message_body += f"{i}. {place}\n"
            
            message_body += f"""
🔗 Enlace directo: https://www.oakhouse.jp/eng/house/tokyo/social-residence?rent_low=&rent_high=&room_size_low=&room_size_high=&vacancy_date%5B%5D=2&vacancy_date%5B%5D=3&mode=do

¡Que tengas un excelente día! 😊"""
        else:
            message_body = """🏠 LISTADO DE RESIDENCIAS DISPONIBLES - Oakhouse

❌ No se encontraron residencias disponibles en este momento.

🔗 Enlace directo: https://www.oakhouse.jp/eng/house/tokyo/social-residence?rent_low=&rent_high=&room_size_low=&room_size_high=&vacancy_date%5B%5D=2&vacancy_date%5B%5D=3&mode=do

¡Que tengas un excelente día! 😊"""

        # Obtener credenciales de Twilio
        twilio_sid = os.environ["TWILIO_ACCOUNT_SID"]
        twilio_token = os.environ["TWILIO_AUTH_TOKEN"]
        whatsapp_to = os.environ["WHATSAPP_TO"]
        
        # Enviar mensaje por WhatsApp
        client = Client(twilio_sid, twilio_token)
        message = client.messages.create(
            from_="whatsapp:+14155238886",  # Número fijo del Sandbox de Twilio
            to=f"whatsapp:{whatsapp_to}",
            body=message_body
        )
        
        print(f"✅ Mensaje enviado exitosamente con SID: {message.sid}")
        print(f"📊 Residencias encontradas: {len(places)}")
        if places:
            print("📋 Listado:")
            for i, place in enumerate(places, 1):
                print(f"  {i}. {place}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    main()
