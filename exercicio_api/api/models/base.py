# api/models/base.py

import logging
import os
import re
import requests

from dotenv import load_dotenv
from django.conf import settings
from groq import Groq

# Carrega variáveis do .env caso queira usar load_dotenv aqui ou no settings
# load_dotenv()

def get_logger(name=__name__):
    """
    Retorna uma instância de logger configurada.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger


class GroqClient:
    """
    Classe responsável por enviar prompts para a API Groq, 
    lendo a chave e o modelo diretamente de settings.
    """
    def __init__(self):
        self.log = get_logger(__name__)
        self.api_key = settings.API_GROQ_KEY
        self.model = settings.LLM  # Carrega o modelo de settings.py
        
        if not self.api_key:
            self.log.error("API_GROQ_KEY não definida em settings.py.")
            raise ValueError("API_GROQ_KEY não encontrada. Verifique seu .env e o settings.py.")

        # Instancia o cliente Groq
        self.client = Groq(api_key=self.api_key)

    def send_prompt(self, prompt: str) -> str:
        """
        Envia um prompt para a Groq API e retorna a resposta do modelo.
        """
        self.log.info(f"Usando modelo {self.model} para completar prompt: {prompt}")
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,  # Usa o modelo definido em settings.LLM
            )
            
            # Captura o texto e remove a tag <think> se usar a LLM do DeepSeek
            response_text = chat_completion.choices[0].message.content
            
            # Remove tudo que estiver entre <think> e </think> (incluindo as tags)
            # A flag DOTALL faz com que o '.' inclua quebras de linha
            response_text = re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL)

            # Retorna a resposta "limpa"
            return response_text.strip()

        except Exception as e:
            self.log.exception("Erro ao consultar LLM via Groq API.")
            return f"Erro na chamada à Groq API: {str(e)}"