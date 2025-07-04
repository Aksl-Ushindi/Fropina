from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse
import openai
from twilio.twiml.messaging_response import MessagingResponse
import uvicorn

app = FastAPI()

# ✨ Clé API OpenAI (à sécuriser dans env var)
openai.api_key = "sk-..."

# 🌟 Prompt système Fropina
FROPINA_PROMPT = """
Tu es Fropina, une experte en soins capillaires naturels pour cheveux afro, bouclés, crêpus et frésis. (...)
"""

@app.post("/whatsapp", response_class=PlainTextResponse)
async def whatsapp_webhook(
    Body: str = Form(..., description="Message texte envoyé par l'utilisateur"),
    From: str = Form(..., description="Numéro de l'expéditeur")
):
    try:
        # OpenAI GPT-4 Call
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": FROPINA_PROMPT},
                {"role": "user", "content": Body}
            ]
        )
        gpt_reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        gpt_reply = f"Oops, erreur GPT : {str(e)}"

    # Réponse Twilio (format XML text/plain)
    twilio_response = MessagingResponse()
    twilio_response.message(gpt_reply)
    return str(twilio_response)

# 🚀 Localhost pour test
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
