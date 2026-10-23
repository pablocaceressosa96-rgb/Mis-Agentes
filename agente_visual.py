import os
import requests
try:
    from groq import Groq
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "groq", "requests"])
    from groq import Groq

# 1. CREDENCIALES
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "TU_API_KEY_DE_GROQ_AQUÍ")
MAKE_WEBHOOK_URL = os.environ.get("MAKE_WEBHOOK_URL", "PEGA_AQUÍ_TU_URL_DE_MAKE")

# 2. INICIALIZAR EL CLIENTE DE GROQ
client = Groq(api_key=GROQ_API_KEY)
tema_cliente = "Dueños de agencias de marketing digital"

try:
    # PASO 1: AGENTE INVESTIGADOR
    prompt_investigador = f"Actúa como un Analista del Consumidor experto. Analiza los problemas principales que tienen los clientes de: {tema_cliente}. Devuelve una lista de las 3 necesidades más urgentes."
    response_1 = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt_investigador}],
        model="llama-3.1-70b-versatile",
        temperature=0.4
    )
    analisis_mercado = response_1.choices.message.content

    # PASO 2: AGENTE REDACTOR
    prompt_redactor = f"Actúa como un Copywriter profesional. Basándote en: {analisis_mercado}, escribe una propuesta de servicio breve e irresistible para WhatsApp o correo, en español, con emojis y hashtags."
    response_2 = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt_redactor}],
        model="llama-3.1-70b-versatile",
        temperature=0.6
    )
    resultado_final = response_2.choices.message.content

    # PASO 3: ENVIAR AL SOFTWARE VISUAL
    payload = {"status": "success", "tema": tema_cliente, "resultado": str(resultado_final)}
    requests.post(MAKE_WEBHOOK_URL, json=payload)
    print("Envío exitoso a Make.com")

except Exception as e:
    print("Error:", e)
