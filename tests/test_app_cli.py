from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

import pytest


@pytest.fixture()
def app_main(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    module_name = "app.__main__"
    if module_name in sys.modules:
        del sys.modules[module_name]
    module = importlib.import_module(module_name)
    return module


def test_strip_quotes(app_main):
    assert app_main._strip_quotes('"abc"') == "abc"
    assert app_main._strip_quotes("'abc'") == "abc"
    assert app_main._strip_quotes("abc") == "abc"


def test_load_dotenv_supports_export_quotes_and_comments(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for key in ["LLM_PROVIDER", "MODEL_INTERVIEWER", "SILICONFLOW_API_KEY", "SILICONFLOW_BASE_URL"]:
        monkeypatch.delenv(key, raising=False)
    env_path = tmp_path / ".env"
    env_path.write_text(
        "\n".join(
            [
                "export LLM_PROVIDER=siliconflow",
                "MODEL_INTERVIEWER=\"Qwen/Qwen2.5-7B-Instruct\"",
                "SILICONFLOW_API_KEY='sk-test'",
                "SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1 # comment",
            ]
        ),
        encoding="utf-8",
    )

    module_name = "app.__main__"
    if module_name in sys.modules:
        del sys.modules[module_name]
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    module = importlib.import_module(module_name)

    assert os.environ["LLM_PROVIDER"] == "siliconflow"
    assert os.environ["MODEL_INTERVIEWER"] == "Qwen/Qwen2.5-7B-Instruct"
    assert os.environ["SILICONFLOW_API_KEY"] == "sk-test"
    assert os.environ["SILICONFLOW_BASE_URL"] == "https://api.siliconflow.cn/v1"


def test_validate_runtime_reports_missing_key(app_main, monkeypatch, tmp_path):
    monkeypatch.setenv("LLM_PROVIDER", "siliconflow")
    monkeypatch.delenv("SILICONFLOW_API_KEY", raising=False)
    monkeypatch.setenv("MODEL_INTERVIEWER", "Qwen/Qwen2.5-7B-Instruct")
    (tmp_path / "notes_clean_v2").mkdir()
    monkeypatch.chdir(tmp_path)

    issues = app_main._validate_runtime("prod")
    assert any("SILICONFLOW_API_KEY" in issue for issue in issues)


def test_validate_runtime_accepts_valid_siliconflow(app_main, monkeypatch, tmp_path):
    (tmp_path / "notes_clean_v2").mkdir()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LLM_PROVIDER", "siliconflow")
    monkeypatch.setenv("MODEL_INTERVIEWER", "Qwen/Qwen2.5-7B-Instruct")
    monkeypatch.setenv("SILICONFLOW_API_KEY", "sk-test")
    monkeypatch.setenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")

    issues = app_main._validate_runtime("prod")
    assert issues == []


def test_ensure_runtime_requires_index(app_main, monkeypatch, tmp_path):
    (tmp_path / "notes_clean_v2").mkdir()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LLM_PROVIDER", "siliconflow")
    monkeypatch.setenv("MODEL_INTERVIEWER", "Qwen/Qwen2.5-7B-Instruct")
    monkeypatch.setenv("SILICONFLOW_API_KEY", "sk-test")

    with pytest.raises(app_main.ConfigError, match="build-index"):
        app_main._ensure_runtime_ok("prod", require_index=True)
