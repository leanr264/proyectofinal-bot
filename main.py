
import telebot
from Sentimentanalyzer import AnalizadorSentimiento


TOKEN = "7692994606:AAFi-7Z-a9OciK-4PREMYqr3mUXKMUGHmxI"

bot = telebot.TeleBot(TOKEN)
analizador = AnalizadorSentimiento()


#con esto prende la maquina ah
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
     message,
        "👋 ¡Hola! Soy un bot parte del *Capstone Project* 🧠\n\n"
        "Usá el comando /analizar seguido de un texto para saber su sentimiento.\n"
        " para analizar imágenes.\n"
        "O enviá un mensaje para conversar con nuestro proyecto sobre consultas informáticas 💬\n",
    parse_mode="Markdown"
)


#Comando especifico para el bot de analisis de sentimiento :P
@bot.message_handler(commands=["analizar"])
def analizar_command(message):
    texto = message.text.replace("/analizar", "").strip()

    if not texto:
        bot.reply_to(
            message,
            "⚠️ Por favor escribí algo después del comando.\n\nEjemplo:\n`/analizar Hoy no quiero laburar, porque esta soleado`",
            parse_mode="Markdown"
        )
        return

    resultado = analizador.analizar(texto)
    bot.reply_to(message, f"🧠 *Análisis de Sentimiento:*\n{resultado}", parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def respuesta_general(message):
    bot.reply_to(
        message,
        " Puedo analizar tus oraciones.\nUsá el comando `/analizar` seguido del texto que quieras analizar.",
        parse_mode="Markdown"
    )


print(" Bot iniciado... Esperando mensajes en Telegram.")
bot.infinity_polling()
