
CAPSTONE PROJECT SAMSUNG INNOVATION CAMPUS (CODEX DEBUG)


  Este es un bot de telegram el cual cumple varias funciones:
      - Entre ellas se encuentra la de analizar imagenes y responder con un informe conciso sobre lo que hay en la imagen.
      - Analizar audios los cuales responde mediante el uso de un dataset sobre informatica
      - Analiza emociones en los mensajes de texto que le compartas y responde con la emocion que detecta y su confianza/seguridad en su resultado.


Todo esto realizdo mediante diferentes clases las cuales son llamadas a un archivo principal (main.py) el cual se debe ejecutar despues de descargar los "requirements.txt".

Este repositorio aloja el código fuente completo de un ChatBot inteligente para Telegram diseñado para responder consultas específicas de índole informática y realizar tareas avanzadas de procesamiento de lenguaje natural y multimedia, como el análisis de sentimientos y el procesamiento de imágenes y voz.

    El bot se ha desarrollado con una estructura modular y escalable, enfocándose en la eficiencia en la respuesta mediante la lectura directa de una base de conocimiento estructurada en formato JSON. Esta aproximación garantiza respuestas precisas y contextuales dentro del dominio informático definido.

🌟 FUNCIONALIDADES PRINCIPALES
    El proyectofinal-bot no es solo un sistema de preguntas y respuestas; integra varias capacidades avanzadas para ofrecer una interacción rica y útil:

ASISTENCIA INFORMÁTICA CON BASE DE CONOCIMIENTO (JSON):

    El bot recibe consultas textuales y utiliza un archivo knowledge_base.json como su fuente principal de verdad.

    Limitación Clave: El bot está configurado para responder solo a temas que se encuentren explícitamente definidos en este JSON. Cualquier consulta fuera de este ámbito resultará en una respuesta estándar de fuera de tema, asegurando la calidad y relevancia de la información proporcionada.

ANÁLISIS DE SENTIMIENTOS:

    Permite al bot indicar qué sentimiento (positivo, negativo, neutro) transmite el mensaje del usuario. Esto es vital para monitorizar la satisfacción del usuario y adaptar futuras interacciones.

PROCESAMIENTO DE VOZ Y RESPUESTA (ASISTENCIA INFORMÁTICA):

    El bot puede recibir mensajes de voz de Telegram, transcribirlos y, posteriormente, procesar la transcripción como una consulta informática normal, respondiendo según la información contenida en el JSON.

ANÁLISIS DE IMAGEN:

    El bot está habilitado para recibir y procesar imágenes, aunque la funcionalidad específica de esta característica puede ser expandida (ej. descripción de contenido, detección de objetos).

⚙️ ESTRUCTURA DEL REPOSITORIO
    La organización del proyecto sigue patrones limpios de desarrollo de bots:

/src: Contiene los módulos principales de Python, incluyendo la lógica del dispatcher de Telegram y las funciones de manejo de handlers.

/data: Directorio esencial. Aquí se aloja el archivo knowledge_base.json, la base de conocimiento que alimenta las respuestas del bot.

/assets: Usado para almacenar cualquier recurso estático necesario (imágenes de ejemplo, modelos, etc.).

requirements.txt: Lista de dependencias de Python necesarias para la ejecución.

🚀 GUÍA DE PUESTA EN MARCHA (SETUP)
    Sigue estos pasos para desplegar y probar el bot en tu entorno local.

1. CLONAR EL REPOSITORIO
    Abre tu terminal y ejecuta:

Bash

git clone https://github.com/leanr264/proyectofinal-bot.git
cd proyectofinal-bot
2. CONFIGURACIÓN DEL ENTORNO
    Se recomienda usar un entorno virtual para aislar las dependencias:

Bash

python -m venv venv
source venv/bin/activate  # En Linux/macOS
# o .\venv\Scripts\activate en Windows
3. INSTALAR DEPENDENCIAS
    Instala todas las librerías necesarias:

Bash

pip install -r requirements.txt
4. CONFIGURACIÓN DE CREDENCIALES Y BASES DE DATOS
    Este paso es crítico. Debes proporcionar el token de Telegram Bot y cualquier otra clave de API requerida (ej. para análisis de voz/imagen si usas servicios externos).

    Crea un archivo llamado .env en la raíz del proyecto.

    Añade la siguiente variable, reemplazando el valor por tu token real:

TELEGRAM_BOT_TOKEN="TU_TOKEN_DE_TELEGRAM_AQUI"
5. POBLAR LA BASE DE CONOCIMIENTO
    Asegúrate de que el archivo data/knowledge_base.json esté correctamente estructurado con las preguntas clave y sus respectivas respuestas informáticas.

6. EJECUTAR EL BOT
    Una vez configurado, ejecuta el script principal:

Bash

python run_bot.py 
# (Asumiendo que el punto de entrada principal del bot se llama run_bot.py)
    Tu bot estará ahora activo y listo para recibir mensajes en Telegram.
    

  




