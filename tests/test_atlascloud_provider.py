import importlib.util
import os
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


class FakeCompletions:
    def __init__(self, client):
        self.client = client

    def create(self, **kwargs):
        self.client.requests.append(kwargs)
        message = types.SimpleNamespace(content="atlas response")
        choice = types.SimpleNamespace(message=message)
        return types.SimpleNamespace(choices=[choice])


class FakeChat:
    def __init__(self, client):
        self.completions = FakeCompletions(client)


class FakeOpenAI:
    calls = []

    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key
        self.base_url = base_url
        self.requests = []
        self.chat = FakeChat(self)
        FakeOpenAI.calls.append(self)


def load_llm_link(module_name: str, relative_path: str):
    openai_module = types.ModuleType("openai")
    openai_module.OpenAI = FakeOpenAI
    dotenv_module = types.ModuleType("dotenv")
    dotenv_module.load_dotenv = lambda *args, **kwargs: None
    spec = importlib.util.spec_from_file_location(module_name, ROOT / relative_path)

    with patch.dict(sys.modules, {"openai": openai_module, "dotenv": dotenv_module}):
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)

    return module


class AtlasCloudProviderTests(unittest.TestCase):
    def setUp(self):
        FakeOpenAI.calls.clear()

    def test_personality_test_routes_atlascloud_alias(self):
        module = load_llm_link("personality_test_llm_link", "Personality_test/llm_link.py")

        with patch.dict(
            os.environ,
            {
                "ATLAS_CLOUD_API_KEY": "atlas-key",
                "ATLAS_CLOUD_API_BASE": "https://atlas.example/v1",
                "ATLAS_CLOUD_MODEL": "deepseek-ai/deepseek-v4-pro",
            },
            clear=True,
        ):
            response = module.get_rsp("hello", "atlas-cloud")

        self.assertEqual(response, "atlas response")
        self.assertEqual(FakeOpenAI.calls[0].api_key, "atlas-key")
        self.assertEqual(FakeOpenAI.calls[0].base_url, "https://atlas.example/v1")
        self.assertEqual(FakeOpenAI.calls[0].requests[0]["model"], "deepseek-ai/deepseek-v4-pro")
        self.assertEqual(FakeOpenAI.calls[0].requests[0]["messages"], [{"role": "user", "content": "hello"}])

    def test_personality_changes_uses_atlascloud_defaults(self):
        module = load_llm_link("personality_changes_llm_link", "Personality_changes/llm_link.py")

        with patch.dict(os.environ, {"ATLASCLOUD_API_KEY": "atlas-key"}, clear=True):
            response = module.get_rsp(
                "next question",
                "ATLASCLOUD",
                "system prompt",
                [{"role": "assistant", "content": "previous answer"}],
            )

        self.assertEqual(response, "atlas response")
        self.assertEqual(FakeOpenAI.calls[0].api_key, "atlas-key")
        self.assertEqual(FakeOpenAI.calls[0].base_url, "https://api.atlascloud.ai/v1")
        self.assertEqual(FakeOpenAI.calls[0].requests[0]["model"], "qwen/qwen3.5-flash")
        self.assertEqual(
            FakeOpenAI.calls[0].requests[0]["messages"],
            [
                {"role": "system", "content": "system prompt"},
                {"role": "assistant", "content": "previous answer"},
                {"role": "user", "content": "next question"},
            ],
        )


if __name__ == "__main__":
    unittest.main()
