# Import correcto para evitar el aviso "types no se exporta"
from telebot import types
import os
from typing import Optional
from message_handler import MessageHandler
# Importamos la clase de texto para la interconexión
from manejador_texto import ManejadorDeTexto


class ManejadorDeAudio(MessageHandler):
    """
    Esta clase se encarga de procesar un mensaje de voz,
    transcribirlo con Groq y pasarlo al ManejadorDeTexto
    para que genere una respuesta.
    """

    def __init__(self, groq):
        super().__init__(groq)
        print("Manejador de Audio creado. ¡Listo para escuchar!")
        self.text_handler = ManejadorDeTexto(groq)

    # Usamos types.Message
    def procesar_entrada(self, bot, message: types.Message):
        """
        Maneja un mensaje de voz completo de Telegram.
        """
        chat_id = message.chat.id
        print(f"Usuario [{chat_id}] envió un mensaje de voz.")

        if not self._groq:
            return "Lo siento, el servicio de audio no está configurado."

        try:
            # Animación de "transcribiendo..."
            bot.send_chat_action(chat_id, "typing")

            # Transcribir el audio
            transcription = self._download_and_transcribe(bot, message)

            if not transcription:
                return "Lo siento, no pude entender tu audio. 🎤 Intenta de nuevo."

            bot.send_message(message.chat.id, transcription)
            print(f"Audio transcrito como: '{transcription}'")

            # Crear un "mensaje simulado" con la transcripción de texto
            new_message = types.Message(
                message_id=message.message_id,
                from_user=message.from_user,
                date=message.date,
                chat=message.chat,
                content_type='text',
                options={},
                json_string='{}'  # no se usa, pero requerido internamente
            )
            new_message.text = transcription  # sobreescribimos el texto

            # Pasamos el mensaje al ManejadorDeTexto.
            respuesta = self.text_handler.procesar_entrada(bot, new_message)

            # Enviamos la respuesta final
            return respuesta

        except Exception as e:
            print(f"Error al responder audio en Telegram: {e}")
            return "Lo siento, tuve un error al procesar tu audio."

    # MÉTODO INTERNO (PRIVADO)
    def _download_and_transcribe(self, bot, message: types.Message) -> Optional[str]:
        """
        Descarga, guarda temporalmente, transcribe con Groq (Whisper)
        y borra el archivo de audio.
        """
        temp_file = f"temp_voice_{message.chat.id}.ogg"
        try:
            # 1. Descargar
            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(
                file_info.file_path)  # file_path existe# type: ignore

            # 2. Guardar temporalmente
            with open(temp_file, "wb") as f:
                f.write(downloaded_file)

            # 3. Transcribir
            with open(temp_file, "rb") as file:
                transcription = self._groq.audio.transcriptions.create(  # type: ignore
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
                os.remove(temp_file)
            return None
