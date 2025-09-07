import os
from twilio.rest import Client

def main():
    """Tester para verificar que todos los secrets están configurados correctamente"""
    
    # Obtener todos los secrets
    twilio_sid = os.environ.get("TWILIO_ACCOUNT_SID", "❌ NO CONFIGURADO")
    twilio_token = os.environ.get("TWILIO_AUTH_TOKEN", "❌ NO CONFIGURADO")
    whatsapp_to = os.environ.get("WHATSAPP_TO", "❌ NO CONFIGURADO")
    search_term = os.environ.get("SEARCH_TERM", "❌ NO CONFIGURADO")
    scraper_enabled = os.environ.get("SCRAPER_ENABLED", "❌ NO CONFIGURADO")
    
    # Crear mensaje de prueba
    test_message = f"""🧪 TESTER DE SECRETS - Oakhouse Notifier

¡Hola! 👋 Este es un mensaje de prueba para verificar que todos los secrets están configurados correctamente.

📋 Estado de los secrets:
• TWILIO_ACCOUNT_SID: {'✅ Configurado' if twilio_sid != '❌ NO CONFIGURADO' else '❌ NO CONFIGURADO'}
• TWILIO_AUTH_TOKEN: {'✅ Configurado' if twilio_token != '❌ NO CONFIGURADO' else '❌ NO CONFIGURADO'}
• WHATSAPP_TO: {whatsapp_to}
• SEARCH_TERM: {search_term}
• SCRAPER_ENABLED: {scraper_enabled}

🚀 El sistema está funcionando correctamente y te notificará cuando encuentre habitaciones disponibles para '{search_term}'.

¡Que tengas un excelente día! 😊"""

    try:
        # Enviar mensaje de prueba
        client = Client(twilio_sid, twilio_token)
        message = client.messages.create(
            from_="whatsapp:+14155238886",  # Número fijo del Sandbox de Twilio
            to=f"whatsapp:{whatsapp_to}",
            body=test_message
        )
        print(f"✅ Mensaje de prueba enviado exitosamente con SID: {message.sid}")
        return True
        
    except Exception as e:
        print(f"❌ Error enviando mensaje de prueba: {str(e)}")
        return False

if __name__ == "__main__":
    main()
