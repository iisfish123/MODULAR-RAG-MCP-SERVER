import importlib
import pytest


TOP_LEVEL_PACKAGES = [
    "mcp_server",
    "core",
    "ingestion",
    "libs",
    "observability",
]


@pytest.mark.parametrize("package_name", TOP_LEVEL_PACKAGES)
def test_import_top_level_package(package_name: str):
    mod = importlib.import_module(package_name)
    assert mod is not None, f"Failed to import {package_name}"


SUB_PACKAGES = [
    "mcp_server.tools",
    "core.query_engine",
    "core.response",
    "core.trace",
    "ingestion.chunking",
    "ingestion.transform",
    "ingestion.embedding",
    "ingestion.storage",
    "libs.loader",
    "libs.llm",
    "libs.embedding",
    "libs.splitter",
    "libs.vector_store",
    "libs.reranker",
    "libs.evaluator",
    "observability.dashboard",
    "observability.evaluation",
]


@pytest.mark.parametrize("package_name", SUB_PACKAGES)
def test_import_sub_package(package_name: str):
    mod = importlib.import_module(package_name)
    assert mod is not None, f"Failed to import {package_name}"


def test_config_directory_exists():
    import os

    config_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config"
    )
    assert os.path.isdir(config_dir), f"config directory not found at {config_dir}"

    prompts_dir = os.path.join(config_dir, "prompts")
    assert os.path.isdir(prompts_dir), f"config/prompts directory not found at {prompts_dir}"


def test_prompt_files_exist():
    import os

    project_root = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    )
    prompt_files = [
        "config/prompts/image_captioning.txt",
        "config/prompts/chunk_refinement.txt",
        "config/prompts/rerank.txt",
    ]
    for pf in prompt_files:
        full_path = os.path.join(project_root, pf)
        assert os.path.isfile(full_path), f"Prompt file not found: {full_path}"


def test_prompt_files_readable():
    import os

    project_root = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    )
    prompt_dir = os.path.join(project_root, "config", "prompts")
    for fname in os.listdir(prompt_dir):
        fpath = os.path.join(prompt_dir, fname)
        with open(fpath, "r") as f:
            content = f.read()
        assert len(content) > 0, f"Prompt file is empty: {fpath}"
