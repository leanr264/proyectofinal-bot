import base64
from typing import Optional, Tuple
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
        descripcion, clasificacion = self.describir_y_clasificar_imagen(
            imagen_base64)

        if not descripcion:
            return "No pude analizar la imagen. Intenta con otra o verifica la API de Groq."

        if clasificacion == "técnica":
            return f"**🧠 Análisis Técnico de Imagen:**\n\n{descripcion}"
        else:
            return f"**📷 La Imagen es general:**\n\n no estoy diseñado para analizar este tipo de imagenes."

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

    def describir_y_clasificar_imagen(self, imagen_base64: str) -> Tuple[Optional[str], str]:
        """
        Usa el modelo de visión de Groq para describir y clasificar la imagen en una sola llamada.
        Devuelve una tupla: (descripcion, clasificacion)
        """
        if not self._groq:
            return None, "general"

        try:
            prompt = (
                "Analiza cuidadosamente la siguiente imagen y realiza dos tareas:\n"
                "Proporciona una descripción clara y detallada en español.\n"
                "Indica si la imagen es de tipo **técnica** o **general**, "
                "según el siguiente criterio:\n"
                "- Técnica: contiene elementos informáticos, código, diagramas, pantallas, hardware, errores de sistema, redes, etc.\n"
                "- General: no tiene relación con temas informáticos o técnicos.\n\n"
                "Formato de respuesta esperado (respeta exactamente este formato):\n\n"
                "**Descripción:** <texto descriptivo>(enfócandose en identificar el problema o componente, junto con la posible solución o explicación del mismo.)\n"
                "**Clasificación:** <técnica|general>"
            )

            respuesta = self._groq.chat.completions.create(
                model=self.modelo_vision,
                messages=[
                    {"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {
                            "url": f"data:image/jpeg;base64,{imagen_base64}"}}
                    ]}
                ],
                temperature=0.7,
                max_tokens=2000
            )

            contenido = respuesta.choices[0].message.content.strip()

            # Extraer partes del texto
            descripcion = ""
            clasificacion = "general"

            if "**Descripción:**" in contenido:
                partes = contenido.split("**Clasificación:**")
                descripcion = partes[0].replace("**Descripción:**", "").strip()
                if len(partes) > 1:
                    clasificacion_texto = partes[1].strip().lower()
                    if "técnica" in clasificacion_texto:
                        clasificacion = "técnica"

            return descripcion, clasificacion

        except Exception as e:
            print(f"Error al describir/clasificar imagen con Groq: {e}")
            return None, "general"
