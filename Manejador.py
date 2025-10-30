import json
import os
import telebot
import requests

# --- Estas son las variables "externas" que mencionaste ---
# (Deberías definirlas en tu script principal)
# GROQ_API_KEY = "tu_llave_de_groq"
# GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
# PATH_DATASET = "dataset.json"

class ManejadorDeTexto:
    """
    Esta clase se encarga de procesar un texto y decidir
    si responde desde un dataset local o desde la IA de Groq.
    """

    def __init__(self, dataset, groq_api_key, groq_api_url):
        print("Manejador de Texto creado. ¡Listo para trabajar!")
        self.dataset = dataset
        self.groq_key = groq_api_key
        self.groq_url = groq_api_url


    def responder_texto_telegram(self, message: telebot.types.Message):
        """
        Maneja un mensaje de texto completo:
        1. Obtiene el texto.
        2. Muestra "escribiendo...".
        3. Procesa la respuesta.
        4. Envía la respuesta por Telegram.
        """
        pregunta = message.text
        chat_id = message.chat.id
        print(f"Usuario [{chat_id}] dice: {pregunta}")

        try:
            # 1. Animación de "escribiendo..."
            # Usa el bot que guardamos en self.bot
            self.bot.send_chat_action(chat_id, "typing")
            
            # 2. Procesa el mensaje llamando a su propio método interno
            # Usa self.procesar_mensaje
            respuesta = self.procesar_mensaje(pregunta)
            
            # 3. Envía la respuesta por Telegram
            # Usa self.bot
            self.bot.reply_to(message, respuesta)
        
        except Exception as e:
            print(f"Error al responder en Telegram: {e}")
            self.bot.reply_to(message, "Lo siento, tuve un error al procesar tu solicitud.")

    # 2. Creamos un método "privado" para buscar en el dataset
    # (El _ al inicio es una convención para decir "este método es para uso interno")
    def _buscar_en_dataset(self, pregunta: str) -> str | None:
        """Busca la pregunta en el dataset. Devuelve la respuesta o None."""
        pregunta_limpia = pregunta.strip().lower()
        for item in self.dataset:
            if item.get('pregunta', '').strip().lower() == pregunta_limpia:
                return item['respuesta']
        return None  # No se encontró nada

    # 3. Creamos un método "privado" para llamar a Groq
    def _llamar_a_groq(self, mensaje: str) -> str:
        """Llama a la API de Groq y devuelve la respuesta."""
        headers = {
            'Authorization': f'Bearer {self.groq_key}',
            'Content-Type': 'application/json'
        }
        data = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": mensaje}]
        }
        try:
            resp = requests.post(self.groq_url, headers=headers, json=data, timeout=20)
            if resp.status_code == 200:
                return resp.json()['choices'][0]['message']['content'].strip()
            else:
                return f"[Error Groq {resp.status_code}]"
        except Exception as e:
            return f"[Error de conexión a Groq: {e}]"

    # 4. ¡EL MÉTODO PRINCIPAL!
    # Este es el único método que llamarás desde fuera de la clase.
    # Recibe el mensaje del usuario y decide qué hacer.
    def procesar_mensaje(self, mensaje_usuario: str) -> str:
        """
        Procesa el mensaje del usuario.
        Primero intenta responder desde el dataset, si falla, consulta a Groq.
        """
        # Paso A: Intentar responder con el dataset
        respuesta_dataset = self._buscar_en_dataset(mensaje_usuario)
        
        if respuesta_dataset:
            # ¡Éxito! Lo encontramos en el dataset
            print("Respondiendo desde el Dataset...")
            return respuesta_dataset
        else:
            # Paso B: No estaba en el dataset, vamos a Groq
            print("Dataset no tiene la respuesta, consultando a Groq...")
            return self._llamar_a_groq(mensaje_usuario)

    # Este método estático está perfecto como lo tenías.
    # Sirve como una "herramienta" extra que la clase ofrece.
    @staticmethod
    def cargar_dataset(path_dataset):
        try:
            with open(path_dataset, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: El archivo no se encontró en la ruta {path_dataset}")
            return []
        except Exception as e:
            print(f"Ocurrió un error al cargar el dataset: {e}")
            return []

  