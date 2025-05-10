from fastapi import FastAPI, Request
import openai
import requests

app = FastAPI()

# Tu API Key de OpenAI
openai.api_key = "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"

# Token de Telegram
TELEGRAM_TOKEN = "7837480577:AAH7sxIaCO6SnLjqL0LQ53H3ZAPe9KCBEoE"
TELEGRAM_API_URL = f"https://api.telegram.org/bot7837480577:AAH7sxIaCO6SnLjqL0LQ53H3ZAPe9KCBEoE"

@app.post(f"/7837480577:AAH7sxIaCO6SnLjqL0LQ53H3ZAPe9KCBEoE")
async def webhook(request: Request):
    data = await request.json()

    # Obtener mensaje y chat_id desde Telegram
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    # Llamada a ChatGPT con el mensaje del usuario
    if text:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en predicciones deportivas. Responde con claridad y precisión."},
                {"role": "user", "content": text}
            ]
        )
        reply = response["choices"][0]["message"]["content"]
    else:
        reply = "No entendí tu mensaje."

    # Responder al usuario en Telegram
    requests.post(
        f"{TELEGRAM_API_URL}/sendMessage",
        json={"chat_id": chat_id, "text": reply}
    )

    return {"ok": True}
