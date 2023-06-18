import os
import openai
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

openai.api_key = os.environ.get("CHAT_GPT_API_KEY")

# Manter um histórico de mensagens para simular uma conversa contínua
conversation_history = [
    {"role": "system", "content": "Você é um assistente de chat."}
]

def get_chat_gpt_response(question: str) -> str | None:
    try:
        # Adicionar a nova mensagem do usuário ao histórico da conversa
        conversation_history.append({"role": "user", "content": question})

        # Usando o endpoint v1/chat/completions para modelos de chat
        response_from_chat_gpt = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )

        # Extraindo a resposta do modelo
        choices = response_from_chat_gpt.get("choices", [])
        if choices:
            message = choices[0].get("message", {})
            text = message.get("content", None)

            # Adicionar a resposta do modelo ao histórico da conversa
            conversation_history.append({"role": "assistant", "content": text})

            return text
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    return None
