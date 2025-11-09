from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key="TU_API_KEY_DE_GEMINI")

menu_cafe_rubio = """
 **MENÚ CAFÉ RUBIO** 

**CAFÉS:**
• Espresso - $2.50
• Americano - $3.00
• Cappuccino - $3.50
• Latte - $4.00
• Mocha - $4.50

**POSTRES:**
• Croissant - $2.80
• Tarta de Chocolate - $4.50
• Cheesecake - $4.00
• Galletas - $1.50

**SANDWICHES:**
• Jamón y Queso - $5.00
• Vegetal - $4.50
• Pollo - $5.50

**PROMOCIONES:**
 Café + Postre = 15% descuento
 Martes de 2x1 en Cappuccinos
"""

def procesar_mensaje(mensaje_cliente):
    mensaje = mensaje_cliente.lower()
    
    
    if "hola" in mensaje:
        return "¡Hola!  Bienvenido/a a Café Rubio. ¿En qué te puedo ayudar?\n\nEscribe:\n• 'menú' para ver nuestro menú\n• 'pedido' para hacer un pedido\n• 'promociones' para ver ofertas\n• 'reserva' para reservar mesa"
    
    elif "menú" in mensaje:
        return menu_cafe_rubio
    
    elif "promociones" in mensaje or "promo" in mensaje:
        return " **PROMOCIONES VIGENTES:**\n• Café + Postre = 15% descuento\n• Martes de 2x1 en Cappuccinos\n• 10% descuento en tu primera compra\n\n¡Solo por hoy! "
    
    elif "pedido" in mensaje or "orden" in mensaje:
        return "¡Perfecto! Para hacer tu pedido escribe:\n'Quiero pedir [producto]'\n\nPor ejemplo: 'Quiero pedir un latte y un croissant'"
    
    elif "reserva" in mensaje or "mesa" in mensaje:
        return " **RESERVAR MESA**\nPara reservar escribe:\n'Reservar para [número] personas, el [día] a las [hora]'\n\nEjemplo: 'Reservar para 2 personas, el viernes a las 7pm'"
    
    elif "quiero pedir" in mensaje:
        return " **PEDIDO RECIBIDO**\n¡Gracias por tu pedido! Lo estamos preparando. Tiempo estimado: 15-20 minutos. "
    
    elif "reservar para" in mensaje:
        return " **RESERVA CONFIRMADA**\n¡Tu mesa está reservada! Te esperamos. Recibirás un recordatorio 1 hora antes. "
    
    else:
 
        try:
            model = genai.GenerativeModel('gemini-pro')
            respuesta = model.generate_content(f"Eres un chatbot amable de Café Rubio. Responde brevemente y útil a: {mensaje_cliente}")
            return respuesta.text
        except:
            return "¡Hola! Soy el asistente de Café Rubio \nPuedo ayudarte con:\n• Menú y precios \n• Hacer pedidos \n• Promociones \n• Reservar mesas \n\n¿Qué necesitas?"

@app.route("/webhook", methods=["POST"])
def webhook():
    
    mensaje_recibido = request.form.get("Body", "").strip()
    numero_cliente = request.form.get("From", "")
    
    print(f"Mensaje de {numero_cliente}: {mensaje_recibido}")
    
    
    respuesta = procesar_mensaje(mensaje_recibido)
    
    
    twilio_respuesta = MessagingResponse()
    twilio_respuesta.message(respuesta)
    
    return str(twilio_respuesta)


@app.route("/", methods=["GET"])
def home():
    return " Chatbot de Café Rubio funcionando correctamente!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)