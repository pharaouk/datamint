import time
from colorama import Fore, Style
import requests
import openai
import os
from dotenv import load_dotenv
import tiktoken



load_dotenv()
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.0))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL", "")
openai.api_key = OPENAI_API_KEY


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def openai_call(
    prompt: str,
    model: str = OPENAI_API_MODEL,
    temperature: float = OPENAI_TEMPERATURE,
    max_tokens: int = 100,
):
    while True:
        try:
                print( "\033[91m\033[1m" + "\n*****TOKEN COUNT*****" + "\033[0m\033[0m")
                tokensCount = num_tokens_from_string(prompt, "cl100k_base")
                print(tokensCount)
                fullTokenCount = tokensCount + max_tokens
                print(fullTokenCount)

                messages = [{"role": "system", "content": prompt}]
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    n=1,
                    stop=None,
                    stream=True
                )
                collected_chunks = []
                collected_messages = ""
                print(f"{Fore.YELLOW}{Style.BRIGHT}Bot: {Style.RESET_ALL}")
                for chunk in response:
                    collected_chunks.append(chunk)  
                    chunk_message = chunk['choices'][0]['delta'] 
                    if "content" in chunk_message:
                        message_text = chunk_message['content']
                        collected_messages += message_text
                        print(f"{message_text}", end="")
                print(f"\n")
                return collected_messages
        except openai.error.RateLimitError:
            print(
                "The OpenAI API rate limit has been exceeded. Waiting 10 seconds and trying again."
            )
            time.sleep(10)  
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 502:
                print(
                    "Received a 502 Bad Gateway error. Waiting 10 seconds and trying again."
                )
                time.sleep(10) 
            else:
                raise e  

   





              
