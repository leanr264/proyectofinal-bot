import base64
from typing import Optional
from message_handler import MessageHandler


class ImageHandler(MessageHandler):
    def __init__(self, groq):
        super().__init__(groq)
        self.modelo_vision = "meta-llama/llama-4-scout-17b-16e-instruct"

    def procesar_entrada(self, bot, mensaje):
        try:
            foto = mensaje.photo[-1]
            info_archivo = bot.get_file(foto.file_id)
            archivo_descargado = bot.download_file(info_archivo.file_path)
            imagen_base64 = self.imagen_a_base64(archivo_descargado)
        except Exception as e:
            return f"Error al descargar o convertir la imagen: {e}"

        if not imagen_base64:
            return "Error interno al codificar la imagen."

        # Interpretar imagen con modelo de visión IA
        descripcion = self.describir_imagen_con_groq(imagen_base64)

        if not descripcion:
            return "No pude analizar la imagen. Intenta con otra o verifica la API de Groq."

        if "mensaje de error" in descripcion.lower() or "código" in descripcion.lower() or "diagrama" in descripcion.lower():
            # Identificar componentes o errores técnicos
            return f"**Análisis Técnico de Imagen:**\n\n{descripcion}"
        else:
            # Describir contenido e interpretar contexto
            return f"**Descripción General de Imagen:**\n\n{descripcion}"

    def imagen_a_base64(self, ruta_o_bytes_imagen):
        """Convierte una imagen a base64 para enviarla a Groq"""
        try:
            if isinstance(ruta_o_bytes_imagen, bytes):
                return base64.b64encode(ruta_o_bytes_imagen).decode('utf-8')
            else:
                with open(ruta_o_bytes_imagen, "rb") as archivo_imagen:
                    return base64.b64encode(archivo_imagen.read()).decode('utf-8')
        except Exception as e:
            print(f"Error al convertir imagen a base64: {e}")
        return None

    def describir_imagen_con_groq(self, imagen_base64: str) -> Optional[str]:
        if not self._groq:
            return "Servicio de visión no disponible (Cliente Groq no inicializado)."

        try:
            prompt = "Por favor, describe esta imagen de manera detallada y clara en español. Si contiene elementos técnicos (circuitos, código, diagramas, hardware, mensajes de error), enfócate en identificar el problema o componente. Si es una imagen general, enfócate en el contenido, contexto y emociones."

            completado_chat = self._groq.chat.completions.create(
                messages=[
                    {"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {
                            "url": f"data:image/jpeg;base64,{imagen_base64}"}}
                    ]}
                ],
                model=self.modelo_vision,
                temperature=0.7,
                max_tokens=2000
            )
            return completado_chat.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error al describir imagen con Groq: {e}")
            return None
