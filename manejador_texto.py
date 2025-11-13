import json
from message_handler import MessageHandler


class ManejadorDeTexto(MessageHandler):
    """
    Esta clase ahora usa Groq como motor principal,
    limitando sus respuestas ÚNICAMENTE al dataset proporcionado
    a través de un system prompt.
    """

    def __init__(self, groq):
        super().__init__(groq)
        self.dataset = "datainformática.json"

        # Convertimos el dataset (que es una lista) a un string JSON.
        try:
            self.dataset_json_string = json.dumps(
                self.dataset, ensure_ascii=False, indent=2)
            print("Dataset serializado correctamente para Groq.")
        except Exception as e:
            print(f"Error al serializar el dataset: {e}")
            self.dataset_json_string = "[]"  # Usar un string vacío en caso de error

        # Creamos la plantilla del System Prompt
        # Usamos {self.dataset_json_string} como marcador de posición.
        self.system_prompt_template = f"""Eres el asistente virtual InfoBot, experto en informática.
Tu tarea es responder preguntas usando EXCLUSIVAMENTE la información del siguiente dataset educativo.

Dataset de referencia:
{self.dataset_json_string}

Reglas importantes:
- Solo puedes responder usando la información contenida en el dataset.
- No menciones al dataset explicitamente, referite a el como "mi base de conocimientos".
- No inventes ni añadas información que no esté allí.
- Si el usuario pregunta algo fuera del dataset, responde: "No tengo esa información en mi base de datos, pero puedo ayudarte con conceptos informáticos básicos."
- Mantén un tono educativo, claro y amigable.
- Usa emojis apropiados para el contexto tecnológico 🤖.
- No incluyas saludos después de la primera interacción.
- Si hay varias respuestas relacionadas, combina la información de manera clara y ordenada.
"""

    def procesar_entrada(self, bot, message):
        """
        Procesa el mensaje del usuario.
        Ahora SIEMPRE consulta a Groq usando el dataset como contexto.
        """
        print("Consultando a Groq con el dataset como contexto...")
        respuesta = self._llamar_a_groq(message)

        """
        Maneja un mensaje de texto completo de Telegram.
        """
        pregunta = message.text
        chat_id = message.chat.id
        print(f"Usuario [{chat_id}] dice: {pregunta}")

        try:
            bot.send_chat_action(chat_id, "typing")
            return respuesta

        except Exception as e:
            print(f"Error al responder en Telegram: {e}")
            return "Lo siento, tuve un error al procesar tu solicitud."

    def _llamar_a_groq(self, mensaje):
        """
        Llama a la API de Groq usando el cliente de Groq.
        """

        if not mensaje or not mensaje.text.strip():
            print("Error: Se intentó llamar a Groq con un mensaje vacío.")
            return "No puedo procesar una solicitud vacía."

        try:
            completion = self._groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": self.system_prompt_template},
                    # Usar el texto extraído
                    {"role": "user", "content": mensaje.text}
                ],
                temperature=0.3,
                max_tokens=500
            )

            # Devolver la respuesta
            return completion.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error al llamar a la API de Groq: {e}")
            return f"[Error al procesar la solicitud con Groq: {e}]"
