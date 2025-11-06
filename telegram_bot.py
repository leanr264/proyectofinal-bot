import telebot as tlb
from image_handler import ImageHandler


class TelegramBot:
    def __init__(self, bot_instance: tlb.TeleBot):
        self._bot = bot_instance

    def start(self):
        print("Bot de Telegram IA (POO) iniciado. Esperando mensajes...")
        self._bot.infinity_polling()

    def definir_entrada(self, groq, mensaje):
        if mensaje.photo:
            handler = ImageHandler(groq)

        respuesta = handler.procesar_entrada(self._bot, mensaje)
        self._bot.send_message(mensaje.chat.id, respuesta)

    def send_response(self, mensaje):
        return
