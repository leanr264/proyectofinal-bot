# Sentimentanalyzer.py

from transformers import pipeline

print("🧠 Cargando el modelo de análisis de sentimiento...")
analizador_de_sentimiento = pipeline("sentiment-analysis", model="pysentimiento/robertuito-sentiment-analysis")
print("✅ Modelo cargado con éxito.")


class AnalizadorSentimiento:
    def __init__(self):
        # Guardamos el modelo dentro de la instancia
        self.analizador = analizador_de_sentimiento

    def analizar(self, frase):
        resultado = self.analizador(frase)[0]
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


# 🧪 Solo se ejecuta si corres este archivo directamente
if __name__ == "__main__":
    analizador = AnalizadorSentimiento()
    texto = input("Escribí una frase para analizar: ")
    resultado = analizador.analizar(texto)
    print(resultado)
