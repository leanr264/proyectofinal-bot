import telebot
from transformers import pipeline
import os



print("🧠 Cargando el modelo de análisis de sentimiento...")
analizador_de_sentimiento = pipeline("sentiment-analysis", model="pysentimiento/robertuito-sentiment-analysis")
print("✅ Modelo cargado con éxito.")
class analizador_Sentimiento:
    def __init__(self, analizar_sentimiento):
        self.analizador_de_sentimiento = analizar_sentimiento

    def analizar_sentimiento(self, frase):
        resultado = analizador_de_sentimiento(frase)[0]
        sentimiento = resultado["label"]
        confianza = resultado["score"]

        if sentimiento.upper() == "POS":
            emoji = "😊"
        elif sentimiento.upper() == "NEG":
            emoji = "😞"
        elif sentimiento.upper() == "NEU":
            emoji = "😐"
        else:
            emoji = "🤔"

        return f"Sentimiento: {sentimiento} {emoji}\nConfianza: {confianza:.2%}"

# 🧪 Prueba del analizador
    if __name__ == "__main__":
        texto = input("Escribí una frase para analizar: ")
        resultado = analizar_sentimiento(texto)
    print(resultado)
