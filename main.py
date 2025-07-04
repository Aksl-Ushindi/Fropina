from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from openai import OpenAI
import uvicorn
import os

load_dotenv()  # 🔐 Charge les variables d'environnement du .env

app = FastAPI()

# 🗝️ Récupère la clé API OpenAI sécurisée
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 💬 Prompt système de Fropina
FROPINA_PROMPT = """
Tu es Fropina, une experte en soins capillaires naturels pour cheveux afro, bouclés, crêpus et frisés.
Tu donnes des conseils simples, naturels, jamais de produits industriels.
Tu parles comme une grande sœur bienveillante, en langage texto.
"""

@app.post("/whatsapp", response_class=PlainTextResponse)
async def whatsapp_webhook(
    Body: str = Form(..., description="Message texte envoyé par l'utilisateur"),
    From: str = Form(..., description="Numéro de l'expéditeur")
):
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # 🔁 Tu peux mettre "gpt-3.5-turbo" si t'as pas accès à gpt-4
            messages=[
                {"role": "system", "content": FROPINA_PROMPT},
                {"role": "user", "content": Body}
            ]
        )
        gpt_reply = response.choices[0].message.content
    except Exception as e:
        gpt_reply = f"Oops, erreur GPT 😢 : {str(e)}"

    twilio_response = MessagingResponse()
    twilio_response.message(gpt_reply)
    return str(twilio_response)

# 🚀 Pour tester en local
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
