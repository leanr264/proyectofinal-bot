import telebot
import os 
# Importamos la clase (que ahora también sabe de Telegram)
from Manejador import ManejadorDeTexto

# --- 1. CONFIGURACIÓN ---
TELEGRAM_TOKEN = "TU_TOKEN_DE_TELEGRAM"
GROQ_API_KEY = "TU_API_KEY_DE_GROQ"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
PATH_DATASET = "dataset.json"

# --- 2. INICIALIZACIÓN ---

# 2a. Cargamos el dataset
print("Cargando dataset...")
dataset_cargado = ManejadorDeTexto.cargar_dataset(PATH_DATASET)

# 2b. Creamos la instancia del bot de Telegram
print("Creando instancia de Telebot...")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# 2c. Creamos la instancia del manejador
# ¡¡IMPORTANTE: Ahora también le pasamos el 'bot'!!
print("Creando el Manejador de Texto...")
manejador = ManejadorDeTexto(
    dataset=dataset_cargado, 
    groq_api_key=GROQ_API_KEY, 
    groq_api_url=GROQ_API_URL,
    bot_instance=bot  # <-- Aquí le pasamos el bot
)

# --- 3. HANDLERS (Los "botones" del bot) ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Responde a los comandos /start y /help."""
    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(message, "¡Hola! Soy un bot IA. Pregúntame algo y responderé usando IA o mi base de datos.")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def responder_texto_principal(message):
    """
    Este es el handler principal. Solo llama a la clase.
    """
    # ¡AQUÍ ESTÁ LA LÍNEA ÚNICA QUE QUERÍAS!
    manejador.responder_texto_telegram(message)

# --- 4. ARRANQUE ---

if __name__ == "__main__":
    print("Bot de Telegram IA (Todo en la clase) iniciado.")
    print("Presiona CTRL + C para detenerlo.")
    bot.infinity_polling()