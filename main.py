from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()  # 👈 Charge le fichier .env

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # ✅ Nouvelle version API

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
            model="gpt-4",
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

# 🧪 Test local (facultatif)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
