import telebot
from image_handler import ImageHandler
from sentiment_analyzer import AnalizadorSentimiento
from manejador_texto import ManejadorDeTexto
from manejador_audio import ManejadorDeAudio


class TelegramBot:
    def __init__(self, token):
        self._bot = telebot.TeleBot(token)

    def start(self):
        print("Bot de Telegram IA (POO) iniciado. Esperando mensajes...")
        self._bot.infinity_polling()

    def send_welcome(self, mensaje):
        """Handler para los comandos /start y /help."""
        welcome_message = (
            "**👋 ¡Bienvenido al ChatBot CodexDebug!**\n\n"
            "Puedo ayudarte con:\n"
            "1. **Consultas Informaticas**. (envía un texto)\n"
            "2. **Análisis de Sentimientos** (envía un texto con el comando /analizar al principio).\n"
            "3. **Transcripción de Voz** (envía una nota de voz).\n"
            "4. **Interpretación de Imágenes** (envía una foto)."
        )
        self._bot.reply_to(mensaje, welcome_message, parse_mode='Markdown')

    def definir_entrada(self, groq, mensaje):
        if mensaje.photo:
            handler = ImageHandler(groq)
        elif mensaje.text:
            texto = mensaje.text.strip()

            if texto.startswith('/analizar'):
                handler = AnalizadorSentimiento()
            else:
                handler = ManejadorDeTexto(groq)

        elif mensaje.voice:
            handler = ManejadorDeAudio(groq)

        respuesta = handler.procesar_entrada(self._bot, mensaje)
        self._bot.reply_to(mensaje, respuesta)
