import telebot
from transformers import pipeline
import os

analizador_de_sentimiento=pipeline("sentiment-analysis",model="ysentimiento/robertuito-sentiment-analysis")
class SentimentAnalyzer:
    def __init__(self, model_name="pysentimiento/robertuito-sentiment-analysis"):
        print("🧠 Cargando el modelo de análisis de sentimiento...")
        self.analizador_de_sentimiento = pipeline("sentiment-analysis", model=model_name)
        print("✅ Modelo cargado con éxito.")
    
    
def analizar_sentimiento(frase):
    resultado = analizador_de_sentimiento(frase)[0]
    sentimiento = resultado["label"]
    confianza = resultado ["score"]

    if sentimiento.lower() == "POS":
        emoji = "^_^"
    elif sentimiento.lower() == "NEG":
        emoji = "(っ °Д °;)っ"
    elif sentimiento.lower() == "NEU":
        emoji = "(•_•)"
    else:
        emoji = "🥴"
    
    return f"sentimiento: {sentimiento.upper()} {emoji}/nConfianza: {confianza:.2%}"

   
    
