import telebot as tlb
import requests
import json
import os
from transformers import pipeline
from groq import Groq
from typing import Optional
import time
from dotenv import load_dotenv


# cargar las variables de entorno
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

if not TELEGRAM_TOKEN:
    raise ValueError("El token de telegram no se cargo")
if not GROQ_API_KEY:
    raise ValueError("No se encuentra API_KEY de Groq")

# instanciar objetos de clases
bot = tlb.TeleBot(TELEGRAM_TOKEN)
groq_client = Groq(api_key=GROQ_API_KEY)
