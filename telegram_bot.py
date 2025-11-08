import telebot as tlb
from image_handler import ImageHandler


class TelegramBot:
    def __init__(self, token):
        self._bot = tlb.TeleBot(token)

    def start(self):
        print("Bot de Telegram IA (POO) iniciado. Esperando mensajes...")
        self._bot.infinity_polling()

    def send_welcome(self, mensaje):
        """Handler para los comandos /start y /help."""
        welcome_message = (
            "**👋 ¡Bienvenido al ChatBot CodexDebug!**\n\n"
            "Puedo ayudarte con:\n"
            "1. **Consultas Informaticas**.\n"
            "2. **Análisis de Sentimientos** (envía un mensaje).\n"
            "3. **Transcripción de Voz** (envía una nota de voz).\n"
            "4. **Interpretación de Imágenes** (envía una foto)."
        )
        self._bot.reply_to(mensaje, welcome_message, parse_mode='Markdown')

    def definir_entrada(self, groq, mensaje):
        if mensaje.photo:
            handler = ImageHandler(groq)

        respuesta = handler.procesar_entrada(self._bot, mensaje)
        self._bot.send_message(mensaje.chat.id, respuesta)

    def send_response(self, respuesta):
        return
