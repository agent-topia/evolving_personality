from openai import OpenAI
from dotenv import load_dotenv
import os



def get_openai_rsp(content : str):
    load_dotenv("para.env")
    api = os.getenv("OPENAI_API_KEY")
    url = os.getenv("OPENAI_BASE_URL")

    client = OpenAI(
        api_key = api,
        base_url = url,
    )

    completion = client.chat.completions.create(
        # model="gpt-5-chat-latest",
        model = "gpt-4",
        messages=[
            {"role": "user", "content": content}
        ],
        temperature=0.6,
    )

    rsp = completion.choices[0].message.content

    return rsp



def get_qwen_rsp(content : str):
    load_dotenv("para.env")
    api = os.getenv("QWEN_API_KEY")
    url = os.getenv("QWEN_BASE_URL")

    client = OpenAI(
        api_key=api,
        base_url=url,
    )

    completion = client.chat.completions.create(
        model="qwen3-235b-a22b-instruct-2507",
        messages=[
            {"role": "user", "content": content}
        ],
        temperature=0.6,
    )

    rsp = completion.choices[0].message.content

    return rsp



def get_llama_rsp(content :str):
    load_dotenv("para.env")
    api = os.getenv("LLAMA_API_KEY")
    url = os.getenv("LLAMA_BASE_URL")

    client = OpenAI(
        api_key=api,
        base_url=url,
    )

    completion = client.chat.completions.create(
        model="meta-llama/llama-4-maverick",
        messages=[
            {"role": "user", "content": content}
        ],
        temperature=0.6,
    )

    rsp = completion.choices[0].message.content

    return rsp



def get_rsp(content : str, model : str):

    if model == "OPENAI":

        return get_openai_rsp(content)

    if model == "QWEN":

        return get_qwen_rsp(content)

    if model == "LLAMA":
        return get_llama_rsp(content)