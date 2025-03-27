from openai import OpenAI
from dotenv import load_dotenv
from io import BytesIO
import requests, json

load_dotenv(override=True)
CLIENT = OpenAI()



def query(chat_history, json_mode=False, model="gpt-4o", temperature=0, max_tokens=4096):
    kwargs = {"response_format": {"type": "json_object"}} if json_mode else {}
    response = CLIENT.chat.completions.create(
        model=model,
        messages=chat_history,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs
    )
    response = response.choices[0].message.content
    if json_mode:
        response = json.loads(response)
    return response


def query_tools(chat_history, toolkit, model="gpt-4o", temperature=0, max_tokens=4096):
    response = CLIENT.chat.completions.create(
            model=model,
            messages=chat_history,
            max_tokens=max_tokens,
            tools=toolkit,
            tool_choice="auto",
            temperature=temperature,
        )
    
    msg = response.choices[0].message.content
    tool_calls = response.choices[0].message.tool_calls
    if not tool_calls: tool_calls = []

    return msg, tool_calls


def generate_image(prompt, size="512x512", model='dall-e-3'):
    response = CLIENT.images.generate(
            model=model,
            prompt=prompt,
            n=1,
            size=size,
            )
    url = response.data[0].url
    response = requests.get(url)
    image = BytesIO(response.content)
    return image
