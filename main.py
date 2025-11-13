import telebot as tlb
import requests
import json
import os
from transformers import pipeline
from groq import Groq
from typing import Optional
import time
from dotenv import load_dotenv
from telegram_bot import TelegramBot


# cargar las variables de entorno
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
# PATH_DATASET = "datainformática.json"

if not TELEGRAM_TOKEN:
    raise ValueError("El token de telegram no se cargo")
if not GROQ_API_KEY:
    raise ValueError("No se encuentra API_KEY de Groq")

# instanciar objetos de clases
bot = TelegramBot(TELEGRAM_TOKEN)
groq_client = Groq(api_key=GROQ_API_KEY)


@bot._bot.message_handler(commands=["start", "help"])
def welcome(mensaje):
    bot.send_welcome(mensaje)


@bot._bot.message_handler(content_types=['photo'])
def manejar_imagen(mensaje):
    bot.definir_entrada(groq_client, mensaje)


# Comando especifico para el bot de analisis de sentimiento
@bot._bot.message_handler(commands=["analizar"])
def analizar_sentimiento(message):
    bot.definir_entrada(groq_client, message)


@bot._bot.message_handler(content_types=['text'])
def responder_consulta(message):
    bot.definir_entrada(groq_client, message)


@bot._bot.message_handler(content_types=['voice'])
def transcribir_audio(message):
    bot.definir_entrada(groq_client, message)


if __name__ == "__main__":
    try:
        # Llamamos al metodo start(), que inicia el polling infinito para recibir mensajes de Telegram
        bot.start()
    except Exception as e:
        print(f"Error fatal al iniciar el bot: {e}")
