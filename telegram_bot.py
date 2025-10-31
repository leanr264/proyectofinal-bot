import telebot as tlb


class TelegramBot:
    def __init__(self, bot_instance: tlb.TeleBot):
        self._bot = bot_instance

    def start(self):
        print("Bot de Telegram IA (POO) iniciado. Esperando mensajes...")
        self._bot.infinity_polling()

    def sendResponse(self, chat_id, response):
        self.bot.send_message(chat_id, response)
