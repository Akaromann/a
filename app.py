import os
import openai
import requests
from flask import Flask, request

# Configura tus claves
TELEGRAM_TOKEN = "TU_TELEGRAM_BOT_TOKEN"
OPENAI_KEY = "TU_OPENAI_API_KEY"
openai.api_key = OPENAI_KEY

app = Flask(__name__)

def get_chatgpt_prediction(user_query):
    prompt = f"""Actúa como un experto en análisis deportivo.
Responde con un pronóstico basado en estadísticas actuales, forma y tendencias.

Consulta: {user_query}

Pronóstico:"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un experto en predicción deportiva."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=200
    )
    return response['choices'][0]['message']['content'].strip()

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    text = data['message'].get('text', '')

    if text:
        reply = get_chatgpt_prediction(text)
        send_message(chat_id, reply)

    return {'ok': True}

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(port=5000)
