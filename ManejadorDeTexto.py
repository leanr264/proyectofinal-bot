import json
import os
import telebot
import requests

class ManejadorDeTexto:
    """
    Esta clase ahora usa Groq como motor principal,
    limitando sus respuestas ÚNICAMENTE al dataset proporcionado
    a través de un system prompt.
    """

    def __init__(self, dataset, groq_api_key, groq_api_url, bot_instance: telebot.TeleBot):
        print("Manejador de Texto creado. ¡Listo para trabajar!")
        self.dataset = dataset
        self.groq_key = groq_api_key
        self.groq_url = groq_api_url
        self.bot = bot_instance

        # --- ¡NUEVO! ---
        # 1. Convertimos el dataset (que es una lista) a un string JSON.
        #    Lo hacemos una sola vez para ser eficientes.
        try:
            self.dataset_json_string = json.dumps(self.dataset, ensure_ascii=False, indent=2)
            print("Dataset serializado correctamente para Groq.")
        except Exception as e:
            print(f"Error al serializar el dataset: {e}")
            self.dataset_json_string = "[]" # Usar un string vacío en caso de error

        # 2. Creamos la plantilla del System Prompt (basado en tu ejemplo)
        #    Usamos {self.dataset_json_string} como marcador de posición.
        self.system_prompt_template = f"""Eres el asistente virtual InfoBot, experto en informática.
Tu tarea es responder preguntas usando EXCLUSIVAMENTE la información del siguiente dataset educativo.

Dataset de referencia:
{self.dataset_json_string}

Reglas importantes:
- Solo puedes responder usando la información contenida en el dataset.
- No inventes ni añadas información que no esté allí.
- Si el usuario pregunta algo fuera del dataset, responde: "No tengo esa información en mi base de datos, pero puedo ayudarte con conceptos informáticos básicos."
- Mantén un tono educativo, claro y amigable.
- Usa emojis apropiados para el contexto tecnológico 🤖.
- No incluyas saludos después de la primera interacción.
- Si hay varias respuestas relacionadas, combina la información de manera clara y ordenada.
"""

    # --- 1. MÉTODOS PRINCIPALES DE TELEGRAM  ---

    def responder_texto_telegram(self, message: telebot.types.Message):
        """
        Maneja un mensaje de texto completo de Telegram.
        """
        pregunta = message.text
        chat_id = message.chat.id
        print(f"Usuario [{chat_id}] dice: {pregunta}")

        try:
            self.bot.send_chat_action(chat_id, "typing")
            
            respuesta = self.procesar_mensaje(pregunta)
            
            self.bot.reply_to(message, respuesta)
        
        except Exception as e:
            print(f"Error al responder en Telegram: {e}")
            self.bot.reply_to(message, "Lo siento, tuve un error al procesar tu solicitud.")

    def procesar_mensaje(self, mensaje_usuario: str) -> str:
        """
        Procesa el mensaje del usuario.
        Ahora SIEMPRE consulta a Groq usando el dataset como contexto.
        """
        print("Consultando a Groq con el dataset como contexto...")
        return self._llamar_a_groq(mensaje_usuario)


    def _llamar_a_groq(self, mensaje: str) -> str:
        """
        Llama a la API de Groq usando el system_prompt pre-cargado
        que contiene todo el dataset.
        """
        
        if not mensaje or not mensaje.strip():
            print("Error: Se intentó llamar a Groq con un mensaje vacío.")
            return "No puedo procesar una solicitud vacía."

        headers = {
            'Authorization': f'Bearer {self.groq_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": "llama-3.3-70b-versatile", 
            "messages": [
                {"role": "system", "content": self.system_prompt_template}, 
                {"role": "user", "content": mensaje}
            ],
            "temperature": 0.3, 
            "max_tokens": 500   
        }
        
        try:
            resp = requests.post(self.groq_url, headers=headers, json=data, timeout=30) 
            
            if resp.status_code == 200:
           
                return resp.json()['choices'][0]['message']['content'].strip()
            else:
              
                print(f"Error: Groq devolvió un status code {resp.status_code}")
                print("Respuesta completa de Groq:")
                print(resp.text)
                
                try:
                    error_info = resp.json()
                    error_message = error_info.get("error", {}).get("message", "Sin detalles")
                    return f"[Error Groq {resp.status_code}: {error_message}]"
                except:
                    return f"[Error Groq {resp.status_code}: {resp.text}]"

        except Exception as e:
            print(f"Error de conexión a Groq: {e}")
            return f"[Error de conexión a Groq: {e}]"


    @staticmethod
    def cargar_dataset(path_dataset):
        """
        Carga el JSON y devuelve SÓLO la lista interna 'dataset'.
        Esto es vital para que __init__ funcione.
        """
        try:
            with open(path_dataset, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data['dataset']
                
        except FileNotFoundError:
            print(f"Error: El archivo no se encontró en la ruta {path_dataset}")
            return []
        except KeyError:
            print("Error: El JSON cargado no tiene una clave llamada 'dataset'.")
            return []
        except Exception as e:
            print(f"Ocurrió un error al cargar el dataset: {e}")
            return []