import os
import json
from dotenv import load_dotenv
from discord.client import Client
from discord.flags import Intents
from discord.message import Message

from openai_api.openapi_connector import get_chat_gpt_response

load_dotenv()

discord_token = os.environ.get("DISCORD_TOKEN")

class CustomDiscordClient(Client):
    async def on_ready(self):
        print(f"Estou conectado ao Discord com o user {self.user}")

    async def on_message(self, message: Message):
        # ID do canal específico em que o bot deve operar
        specific_channel_id = "1120135556320460901"  # Substitua isso pelo ID do canal

        # Verifique se a mensagem foi enviada no canal específico e não foi enviada pelo próprio bot
        if str(message.channel.id) == specific_channel_id and message.author != self.user:
            print(f"Recebi uma mensagem: {message.content}")  # Adicionar esta linha
            prompt = message.content

            # Carregar histórico de conversa do arquivo
            try:
                with open("conversation_history.json", "r") as file:
                    conversation_history = json.load(file)
                    if not conversation_history:
                        conversation_history = []
            except (FileNotFoundError, json.JSONDecodeError):
                conversation_history = []

            # Obter resposta do chatbot
            print("Chamando get_chat_gpt_response...")  # Adicionar esta linha
            chat_gpt_response = get_chat_gpt_response(question=prompt, history=conversation_history)
            print(f"Resposta recebida: {chat_gpt_response}")  # Adicionar esta linha

            # Adicionar resposta ao histórico
            if chat_gpt_response:
                conversation_history.append({"User": prompt, "Bot": chat_gpt_response})

                # Salvar o histórico atualizado no arquivo
                with open("conversation_history.json", "w") as file:
                    json.dump(conversation_history, file)

                # Enviar resposta para o canal Discord
                await message.channel.send(content=chat_gpt_response)
            else:
                print("Nenhuma resposta recebida do chatbot.")  # Adicionar esta linha
        else:
            print("Mensagem ignorada (não está no canal específico ou foi enviada pelo bot).")  # Adicionar esta linha


intents = Intents.default()
intents.message_content = True
custom_discord_client = CustomDiscordClient(intents=intents)
custom_discord_client.run(discord_token)
