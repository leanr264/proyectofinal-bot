# Sentimentanalyzer.py

from transformers import pipeline
# from message_handler import MessageHandler

print("🧠 Cargando el modelo de análisis de sentimiento...")
analizador_de_sentimiento = pipeline(
    "sentiment-analysis", model="pysentimiento/robertuito-sentiment-analysis")
print("✅ Modelo cargado con éxito.")


class AnalizadorSentimiento():
    def __init__(self):
        # super().__init__(groq)
        # Guardamos el modelo dentro de la instancia
        self.analizador = analizador_de_sentimiento

    def procesar_entrada(self, bot, frase):
        # se divide el comando analizar del texto
        texto = frase.text.replace("/analizar", "").strip()

        if not texto:
            bot.reply_to(
                frase,
                "⚠️ Por favor escribí algo después del comando.\n\nEjemplo:\n`/analizar Hoy no quiero laburar, porque esta soleado`",
                parse_mode="Markdown"
            )

        resultado = self.analizador(texto)[0]
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
