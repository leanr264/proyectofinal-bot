import telebot
import os
from typing import Optional
from groq import Groq  # Importamos la librería de cliente de Groq para el audio
from Manejador import ManejadorDeTexto # Importamos tu clase de texto para la interconexión

class ManejadorDeAudio:
    """
    Esta clase se encarga de procesar un mensaje de voz,
    transcribirlo con Groq y pasarlo al ManejadorDeTexto
    para que genere una respuesta.
    """

    def __init__(self, bot_instance: telebot.TeleBot, groq_api_key: str, text_handler_instance: ManejadorDeTexto):
        print("Manejador de Audio creado. ¡Listo para escuchar!")
        self.bot = bot_instance
        self.text_handler = text_handler_instance
        
        # Este cliente usará la LIBRERÍA de Groq, 
        # que es más fácil para 'whisper' (audio)
        try:
            self.groq_client = Groq(api_key=groq_api_key)
            print("Cliente de Groq para audio inicializado.")
        except Exception as e:
            print(f"Error al inicializar el cliente de Groq para audio: {e}")
            self.groq_client = None

    # --- 1. MÉTODO PRINCIPAL DE TELEGRAM ---

    def responder_audio_telegram(self, message: telebot.types.Message):
        """
        Maneja un mensaje de voz completo de Telegram.
        """
        chat_id = message.chat.id
        print(f"Usuario [{chat_id}] envió un mensaje de voz.")

        if not self.groq_client:
            self.bot.reply_to(message, "Lo siento, el servicio de audio no está configurado.")
            return

        try:
            # 1. Animación de "transcribiendo..."
            self.bot.send_chat_action(chat_id, "typing")
            
            # 2. Transcribir el audio
            transcription = self._download_and_transcribe(message)
            
            if not transcription:
                self.bot.reply_to(message, "Lo siento, no pude entender tu audio. 🎤 Intenta de nuevo.")
                return

            print(f"Audio transcrito como: '{transcription}'")
            
            # 3. ¡LA CLAVE!
            #    Ahora que tenemos texto, se lo pasamos al ManejadorDeTexto.
            #    Él se encargará de buscar en el dataset o llamar a la IA (chat).
            respuesta = self.text_handler.procesar_mensaje(transcription)

            # 4. Envía la respuesta final por Telegram
            self.bot.reply_to(message, respuesta)
        
        except Exception as e:
            print(f"Error al responder audio en Telegram: {e}")
            self.bot.reply_to(message, "Lo siento, tuve un error al procesar tu audio.")

    # --- 2. MÉTODO INTERNO (PRIVADO) ---

    def _download_and_transcribe(self, message: telebot.types.Message) -> Optional[str]:
        """
        Descarga, guarda temporalmente, transcribe con Groq (Whisper)
        y borra el archivo de audio.
        """
        temp_file = f"temp_voice_{message.chat.id}.ogg"
        try:
            # 1. Descargar
            file_info = self.bot.get_file(message.voice.file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)
            
            # 2. Guardar temporalmente
            with open(temp_file, "wb") as f:
                f.write(downloaded_file)

            # 3. Transcribir
            with open(temp_file, "rb") as file:
                transcription = self.groq_client.audio.transcriptions.create(
                    file=(temp_file, file.read()),
                    model="whisper-large-v3-turbo",
                    response_format="json",
                    language="es"
                )
            
            # 4. Limpiar
            os.remove(temp_file)
            
            return transcription.text
        
        except Exception as e:
            print(f"Error al descargar o transcribir: {str(e)}")
            if os.path.exists(temp_file):
                os.remove(temp_file) # Asegurarse de borrarlo si falla
            return None