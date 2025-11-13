# **CAPSTONE PROJECT SAMSUNG INNOVATION CAMPUS (CODEX DEBUG)**
# 🤖 **TELEGRAM INFOBOT: ASISTENTE DE INTELIGENCIA ARTIFICIAL**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Groq](https://img.shields.io/badge/AI-Groq-orange?style=for-the-badge)

> Un asistente virtual avanzado diseñado para responder consultas informáticas de manera precisa, restringida y segura, integrando capacidades multimodales (Texto, Voz e Imagen).

---

## 📋 **DESCRIPCIÓN DEL PROYECTO**

Este proyecto consiste en un **ChatBot para Telegram** desarrollado en Python. Su núcleo es un sistema de **Generación Aumentada por Recuperación (RAG)** simplificado, que utiliza la potencia de los LLMs (vía Groq API) pero restringe estrictamente el conocimiento a un dataset local (`datainformática.json`).

El objetivo es ofrecer un asistente educativo o de soporte técnico que **no alucine** información, sino que interprete y exponga datos verídicos previamente curados, además de analizar el contexto emocional del usuario.

---

## 🚀 **CARACTERÍSTICAS PRINCIPALES**

El bot cuenta con cuatro módulos fundamentales de interacción:

* **💬 Respuestas Basadas en Dataset (RAG Estricto)**
    * El bot lee un archivo JSON local con información técnica.
    * Utiliza un *System Prompt* avanzado para instruir a la IA (Llama-3 via Groq) a responder **únicamente** con la información de ese archivo.
    * Si la pregunta está fuera del alcance del dataset, el bot declina amablemente la respuesta.

* **🎭 Análisis de Sentimientos**
    * Cada mensaje recibido es evaluado para detectar el tono emocional del usuario (positivo, negativo, neutral, enojado, confundido).
    * Esto permite futuras implementaciones de atención prioritaria o respuestas empáticas.

* **🎙️ Procesamiento de Voz (Speech-to-Text)**
    * Capacidad para recibir notas de voz de Telegram.
    * Transcribe el audio a texto automáticamente y procesa la consulta informática contenida en él como si fuera texto escrito.

* **📷 Análisis de Imágenes (Visión Artificial)**
    * El usuario puede enviar fotos (ej. componentes de hardware, errores en pantalla).
    * El bot analiza la imagen y ofrece una descripción o solución técnica basada en el contenido visual.

---

## 🛠️ **TECNOLOGÍAS UTILIZADAS**

Este proyecto ha sido construido utilizando las siguientes librerías y herramientas:

* **`pyTelegramBotAPI` (Telebot):** Para la interacción con la API de Telegram.
* **`Requests`:** Para el manejo de peticiones HTTP a la API de Groq.
* **`Groq Cloud API`:** Motor de inteligencia artificial (Modelos Llama-3).
* **`JSON`:** Estructura de datos para el conocimiento base.
* **`OS / IO`:** Manejo de archivos del sistema.

---

## ⚙️ **INSTALACIÓN Y CONFIGURACIÓN**

Sigue estos pasos para ejecutar el bot en tu entorno local:

### **1. Clonar el Repositorio**

```bash
git clone [https://github.com/leanr264/proyectofinal-bot.git](https://github.com/leanr264/proyectofinal-bot.git)
cd proyectofinal-bot
```

2- Crear entorno virtual (RECOMENDADO)

```bash
python -m venv venv
```

# En Windows:

```bash
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```
3-Instalar Dependencias

```bash
pip install pyTelegramBotAPI requests
# (Instalar otras librerías necesarias para audio/imagen si aplica, ej: SpeechRecognition, Pillow)
```

4. Configuración de Variables
Asegúrate de tener tus claves de API listas. Debes configurar las siguientes constantes en tu archivo principal o, preferiblemente, en variables de entorno:

TELEGRAM_TOKEN: Tu token proporcionado por @BotFather.

GROQ_API_KEY: Tu clave API de la plataforma Groq.

PATH_DATASET: La ruta a tu archivo datainformática.json.

📖 MODO DE USO
Una vez que el bot esté corriendo (python Bot_telegram.py), puedes interactuar con él de las siguientes formas:

Comando /start: Inicia la conversación y recibe el mensaje de bienvenida.

Consultas de Texto:

Usuario: "¿Qué es un procesador?" Bot: (Busca en el JSON y genera una respuesta explicativa).

Consultas de Voz: Envía un audio preguntando "¿Cuál es la diferencia entre RAM y ROM?".

Consultas de Imagen: Envía una foto de un componente para que el bot intente identificarlo o explicarlo.

📂 ESTRUCTURA DEL PROYECTO

```text
proyectofinal-bot/
├── Bot_telegram.py       # Script principal (Entry point)
├── ManejadorDeTexto.py   # Clase lógica (Conexión Groq + Dataset)
├── datainformática.json  # Base de conocimiento (Dataset)
├── .gitignore            # Archivos ignorados por Git
└── README.md             # Documentación
```
