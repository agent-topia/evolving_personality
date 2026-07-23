from openai import OpenAI
from dotenv import load_dotenv
import os


ATLAS_CLOUD_BASE_URL = "https://api.atlascloud.ai/v1"
ATLAS_CLOUD_DEFAULT_MODEL = "qwen/qwen3.5-flash"


def _get_env(*names: str, default=None):
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return default


def _normalize_model_name(model: str) -> str:
    return model.replace("-", "_").upper()



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


def get_atlascloud_rsp(content : str, sys_prompt : str, history_msg : list):
    load_dotenv("para.env")
    api = _get_env("ATLASCLOUD_API_KEY", "ATLAS_CLOUD_API_KEY")
    url = _get_env(
        "ATLASCLOUD_API_BASE",
        "ATLAS_CLOUD_API_BASE",
        "ATLASCLOUD_BASE_URL",
        "ATLAS_CLOUD_BASE_URL",
        default=ATLAS_CLOUD_BASE_URL,
    )
    model = _get_env(
        "ATLASCLOUD_MODEL",
        "ATLAS_CLOUD_MODEL",
        default=ATLAS_CLOUD_DEFAULT_MODEL,
    )

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
    normalized_model = _normalize_model_name(model)

    if normalized_model == "OPENAI":

        return get_openai_rsp(content, sys_prompt, history_msg)

    if normalized_model == "QWEN":

        return get_qwen_rsp(content, sys_prompt, history_msg)

    if normalized_model == "LLAMA":
        return get_llama_rsp(content, sys_prompt, history_msg)

    if normalized_model in {"ATLASCLOUD", "ATLAS_CLOUD", "ATLAS"}:
        return get_atlascloud_rsp(content, sys_prompt, history_msg)

    return None
