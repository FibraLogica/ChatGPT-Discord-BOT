import os
import openai
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

openai.api_key = os.environ.get("CHAT_GPT_API_KEY")

def get_chat_gpt_response(question: str, history: List[Dict[str, str]]) -> str | None:
    # Construir a lista de mensagens com histórico de conversa
    messages = [{"role": "system", "content": "Você é um chatbot útil."}]
    for entry in history:
        messages.append({"role": "user", "content": entry["User"]})
        messages.append({"role": "assistant", "content": entry["Bot"]})
    messages.append({"role": "user", "content": question})

    # Fazer a chamada da API OpenAI
    try:
        response_from_chat_gpt = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=100
        )
    except Exception as e:
        return None

    # Extrair a resposta do chatbot
    if response_from_chat_gpt:
        choices = response_from_chat_gpt.get("choices", None)
        if choices and len(choices) > 0:
            message = choices[0].get("message", None)
            if message:
                text = message.get("content", None)
                return text
    return None
