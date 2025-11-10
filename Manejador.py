import json
import os
import telebot
import requests
from fuzzywuzzy import fuzz

class ManejadorDeTexto:
    """
    Esta clase se encarga de procesar un texto y decidir
    si responde desde un dataset local o desde la IA de Groq.
    """

    def __init__(self, dataset, groq_api_key, groq_api_url, bot_instance: telebot.TeleBot):
        print("Manejador de Texto creado. ¡Listo para trabajar!")
        self.dataset = dataset
        self.groq_key = groq_api_key
        self.groq_url = groq_api_url
        self.bot = bot_instance

    # --- 1. MÉTODOS PRINCIPALES DE TELEGRAM ---

    def responder_texto_telegram(self, message: telebot.types.Message):
        """
        Maneja un mensaje de texto completo de Telegram.
        """
        pregunta = message.text
        chat_id = message.chat.id
        print(f"Usuario [{chat_id}] dice: {pregunta}")

        try:
            # 1. Animación de "escribiendo..."
            self.bot.send_chat_action(chat_id, "typing")
            
            # 2. Procesa el mensaje
            respuesta = self.procesar_mensaje(pregunta)
            
            # 3. Envía la respuesta por Telegram
            self.bot.reply_to(message, respuesta)
        
        except Exception as e:
            print(f"Error al responder en Telegram: {e}")
            self.bot.reply_to(message, "Lo siento, tuve un error al procesar tu solicitud.")

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

    # --- 2. MÉTODOS INTERNOS (PRIVADOS) ---

    def _buscar_en_dataset(self, pregunta: str) -> str | None:
        """
        Busca la pregunta en el dataset usando "fuzzy matching" 
        para tolerar errores ortográficos y puntuación.
        """
        # Limpiamos la pregunta del usuario (minúsculas y espacios)
        pregunta_usuario_limpia = " ".join(pregunta.lower().split())

        mejor_puntuacion = 0
        mejor_respuesta = None
        
        # Define qué tan parecida debe ser la pregunta (de 0 a 100).
        UMBRAL_DE_COINCIDENCIA = 85

        for item in self.dataset:
            # Obtenemos y limpiamos la pregunta del dataset
            pregunta_dataset = item.get('pregunta', '')
            pregunta_dataset_limpia = " ".join(pregunta_dataset.lower().split())

            # Calculamos la similitud
            puntuacion = fuzz.token_sort_ratio(pregunta_usuario_limpia, pregunta_dataset_limpia)

            if puntuacion > UMBRAL_DE_COINCIDENCIA and puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_respuesta = item['respuesta']

        return mejor_respuesta

    def _llamar_a_groq(self, mensaje: str) -> str:
        """
        Llama a la API de Groq y devuelve la respuesta, con manejo de errores mejorado.
        """
        
        # 1. Revisar que el mensaje no esté vacío
        if not mensaje or not mensaje.strip():
            print("Error: Se intentó llamar a Groq con un mensaje vacío.")
            return "No puedo procesar una solicitud vacía."

        headers = {
            'Authorization': f'Bearer {self.groq_key}',
            'Content-Type': 'application/json'
        }
        data = {
            "model": "moonshotai/kimi-k2-instruct-0905",
            "messages": [{"role": "user", "content": mensaje}]
        }
        
        try:
            resp = requests.post(self.groq_url, headers=headers, json=data, timeout=20)
            
            if resp.status_code == 200:
                # Éxito
                return resp.json()['choices'][0]['message']['content'].strip()
            else:
                # 2. Imprimir el error real de Groq
                print(f"Error: Groq devolvió un status code {resp.status_code}")
                print("Respuesta completa de Groq:")
                print(resp.text) # <-- ¡Esto nos dirá el problema!
                
                try:
                    error_info = resp.json()
                    error_message = error_info.get("error", {}).get("message", "Sin detalles")
                    return f"[Error Groq {resp.status_code}: {error_message}]"
                except:
                    return f"[Error Groq {resp.status_code}: {resp.text}]"

        except Exception as e:
            print(f"Error de conexión a Groq: {e}")
            return f"[Error de conexión a Groq: {e}]"


    # --- 3. MÉTODO ESTÁTICO (HERRAMIENTA) ---

    @staticmethod
    def cargar_dataset(path_dataset):
        """
        (ESTA ES LA VERSIÓN CORRECTA, SIN DUPLICADOS)
        Carga el JSON y devuelve SÓLO la lista interna 'dataset'.
        """
        try:
            with open(path_dataset, 'r', encoding='utf-8') as f:
                # 1. Cargamos el diccionario completo
                data = json.load(f)
                
                # 2. Devolvemos SOLAMENTE la lista interna "dataset"
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