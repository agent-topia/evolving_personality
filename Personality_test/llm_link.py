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


def _chat(content: str, api_key, base_url, model: str):
    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": content}
        ],
        temperature=0.6,
    )

    return completion.choices[0].message.content



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


def get_atlascloud_rsp(content : str):
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

    return _chat(content, api, url, model)



def get_rsp(content : str, model : str):
    normalized_model = _normalize_model_name(model)

    if normalized_model == "OPENAI":

        return get_openai_rsp(content)

    if normalized_model == "QWEN":

        return get_qwen_rsp(content)

    if normalized_model == "LLAMA":
        return get_llama_rsp(content)

    if normalized_model in {"ATLASCLOUD", "ATLAS_CLOUD", "ATLAS"}:
        return get_atlascloud_rsp(content)
