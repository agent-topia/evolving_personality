from openai import OpenAI
from dotenv import load_dotenv
import os



def get_openai_rsp(content : str, sys_prompt : str, history_msg : list):
    load_dotenv("para.env")
    api = os.getenv("OPENAI_API_KEY")
    url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("OPENAI_MODEL")

    client = OpenAI(
        api_key = api,
        base_url = url,
    )

    rsp = one_dialogue(content, client, model, sys_prompt, history_msg)

    return rsp



def get_qwen_rsp(content : str, sys_prompt : str, history_msg : list):
    load_dotenv("para.env")
    api = os.getenv("QWEN_API_KEY")
    url = os.getenv("QWEN_BASE_URL")
    model = os.getenv("QWEN_MODEL")

    client = OpenAI(
        api_key=api,
        base_url=url,
    )

    rsp = one_dialogue(content, client, model, sys_prompt, history_msg)

    return rsp



def get_llama_rsp(content : str, sys_prompt : str, history_msg : list):
    load_dotenv("para.env")
    api = os.getenv("LLAMA_API_KEY")
    url = os.getenv("LLAMA_BASE_URL")
    model = os.getenv("LLAMA_MODEL")

    client = OpenAI(
        api_key=api,
        base_url=url,
    )


    rsp = one_dialogue(content, client, model, sys_prompt, history_msg)

    return rsp



# 单对话处理
def one_dialogue(content: str, client : OpenAI, model : str, sys_prompt : str, history_msg : list):
    messages = []
    messages.append({"role": "system", "content": sys_prompt})
    for history in history_msg:
        messages.append(history)
    messages.append({"role": "user", "content": content})
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.6
    )
    rsp = completion.choices[0].message.content
    return rsp


def get_rsp(content : str, model : str, sys_prompt : str, history_msg : list):

    if model == "OPENAI":

        return get_openai_rsp(content, sys_prompt, history_msg)

    if model == "QWEN":

        return get_qwen_rsp(content, sys_prompt, history_msg)

    if model == "LLAMA":
        return get_llama_rsp(content, sys_prompt, history_msg)

    return None