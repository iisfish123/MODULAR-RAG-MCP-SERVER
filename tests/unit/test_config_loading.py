import os
import tempfile

import pytest

from core.settings import (
    Settings,
    LLMConfig,
    EmbeddingConfig,
    VectorStoreConfig,
    RetrievalConfig,
    RerankConfig,
    IngestionConfig,
    EvaluationConfig,
    ObservabilityConfig,
    load_settings,
    validate_settings,
)


MINIMAL_YAML = """
llm:
  provider: openai
embedding:
  provider: openai
vector_store:
  provider: chroma
"""

FULL_YAML = """
llm:
  provider: openai
  openai:
    model: gpt-4o
    api_key_env: OPENAI_API_KEY
  ollama:
    base_url: http://localhost:11434
    model: deepseek-r1:latest
embedding:
  provider: openai
  openai:
    model: text-embedding-3-small
    api_key_env: OPENAI_API_KEY
vector_store:
  provider: chroma
  chroma:
    persist_directory: data/db/chroma
retrieval:
  dense:
    top_k: 20
  sparse:
    top_k: 20
  fusion:
    k: 60
  final_top_k: 10
rerank:
  backend: none
  llm:
    prompt_path: config/prompts/rerank.txt
  cross_encoder:
    model: cross-encoder/ms-marco-MiniLM-L-6-v2
    max_length: 512
ingestion:
  chunk_size: 512
  chunk_overlap: 64
  batch_size: 10
  chunk_refiner:
    use_llm: false
  metadata_enricher:
    use_llm: false
evaluation:
  backends:
    - custom
  ragas:
    metrics:
      - faithfulness
      - answer_relevancy
observability:
  log_level: INFO
  trace_enabled: true
  traces_path: logs/traces.jsonl
  app_log_path: logs/app.log
"""


def _write_temp_yaml(content: str) -> str:
    fd, path = tempfile.mkstemp(suffix=".yaml")
    with os.fdopen(fd, "w") as f:
        f.write(content)
    return path


class TestMinimalConfig:
    def test_load_minimal_settings_success(self):
        path = _write_temp_yaml(MINIMAL_YAML)
        try:
            settings = load_settings(path)
            assert settings.llm.provider == "openai"
            assert settings.embedding.provider == "openai"
            assert settings.vector_store.provider == "chroma"
        finally:
            os.unlink(path)

    def test_defaults_applied_for_unspecified(self):
        path = _write_temp_yaml(MINIMAL_YAML)
        try:
            settings = load_settings(path)
            assert settings.retrieval.dense.top_k == 20
            assert settings.retrieval.final_top_k == 10
            assert settings.rerank.backend == "none"
            assert settings.observability.log_level == "INFO"
        finally:
            os.unlink(path)


class TestFullConfig:
    def test_load_full_settings_success(self):
        path = _write_temp_yaml(FULL_YAML)
        try:
            settings = load_settings(path)
            assert settings.llm.provider == "openai"
            assert settings.llm.openai.model == "gpt-4o"
            assert settings.embedding.provider == "openai"
            assert settings.vector_store.provider == "chroma"
            assert settings.vector_store.chroma.persist_directory == "data/db/chroma"
            assert settings.retrieval.dense.top_k == 20
            assert settings.retrieval.sparse.top_k == 20
            assert settings.retrieval.fusion.k == 60
            assert settings.ingestion.chunk_size == 512
            assert settings.ingestion.chunk_overlap == 64
            assert settings.observability.log_level == "INFO"
            assert settings.observability.trace_enabled is True
        finally:
            os.unlink(path)

    def test_evaluation_backends_list(self):
        path = _write_temp_yaml(FULL_YAML)
        try:
            settings = load_settings(path)
            assert "custom" in settings.evaluation.backends
            assert "faithfulness" in settings.evaluation.ragas.metrics
        finally:
            os.unlink(path)


class TestSettingsValidation:
    def test_missing_llm_provider_raises(self):
        content = MINIMAL_YAML.replace("provider: openai", "provider:", 1)
        path = _write_temp_yaml(content)
        try:
            with pytest.raises(ValueError, match="llm.provider"):
                load_settings(path)
        finally:
            os.unlink(path)

    def test_missing_embedding_provider_raises(self):
        content = """llm:
  provider: openai
embedding:
  provider:
vector_store:
  provider: chroma
"""
        path = _write_temp_yaml(content)
        try:
            with pytest.raises(ValueError, match="embedding.provider"):
                load_settings(path)
        finally:
            os.unlink(path)

    def test_missing_vector_store_provider_raises(self):
        content = MINIMAL_YAML.replace("provider: chroma", "provider: ")
        path = _write_temp_yaml(content)
        try:
            with pytest.raises(ValueError, match="vector_store.provider"):
                load_settings(path)
        finally:
            os.unlink(path)

    def test_missing_all_providers_raises_with_all_errors(self):
        content = """
llm:
  provider:
embedding:
  provider:
vector_store:
  provider:
"""
        path = _write_temp_yaml(content)
        try:
            with pytest.raises(ValueError) as excinfo:
                load_settings(path)
            msg = str(excinfo.value)
            assert "llm.provider" in msg
            assert "embedding.provider" in msg
            assert "vector_store.provider" in msg
        finally:
            os.unlink(path)

    def test_empty_fields_treated_as_missing(self):
        path = _write_temp_yaml("llm:\n  provider: ''\nembedding:\n  provider: ''\nvector_store:\n  provider: ''\n")
        try:
            with pytest.raises(ValueError):
                load_settings(path)
        finally:
            os.unlink(path)


class TestSettingsEdgeCases:
    def test_nonexistent_file_raises(self):
        with pytest.raises(FileNotFoundError):
            load_settings("/nonexistent/path/settings.yaml")

    def test_empty_file_raises(self):
        path = _write_temp_yaml("")
        try:
            with pytest.raises(ValueError, match="empty"):
                load_settings(path)
        finally:
            os.unlink(path)

    def test_null_yaml_raises(self):
        path = _write_temp_yaml("null")
        try:
            with pytest.raises(ValueError, match="empty"):
                load_settings(path)
        finally:
            os.unlink(path)

    def test_validate_settings_on_default_raises(self):
        with pytest.raises(ValueError, match="llm.provider"):
            validate_settings(Settings())

    def test_valid_settings_passes_validation(self):
        settings = Settings(
            llm=LLMConfig(provider="openai"),
            embedding=EmbeddingConfig(provider="openai"),
            vector_store=VectorStoreConfig(provider="chroma"),
        )
        validate_settings(settings)

    def test_ollama_config_parsed(self):
        content = """
llm:
  provider: ollama
  ollama:
    base_url: http://localhost:11434
    model: deepseek-r1:latest
embedding:
  provider: ollama
vector_store:
  provider: chroma
"""
        path = _write_temp_yaml(content)
        try:
            settings = load_settings(path)
            assert settings.llm.ollama.base_url == "http://localhost:11434"
            assert settings.llm.ollama.model == "deepseek-r1:latest"
        finally:
            os.unlink(path)


class TestSettingsStructure:
    def test_settings_has_all_top_level_sections(self):
        path = _write_temp_yaml(FULL_YAML)
        try:
            settings = load_settings(path)
            assert isinstance(settings.llm, LLMConfig)
            assert isinstance(settings.embedding, EmbeddingConfig)
            assert isinstance(settings.vector_store, VectorStoreConfig)
            assert isinstance(settings.retrieval, RetrievalConfig)
            assert isinstance(settings.rerank, RerankConfig)
            assert isinstance(settings.ingestion, IngestionConfig)
            assert isinstance(settings.evaluation, EvaluationConfig)
            assert isinstance(settings.observability, ObservabilityConfig)
        finally:
            os.unlink(path)

    def test_settings_repr_no_exception(self):
        settings = Settings(
            llm=LLMConfig(provider="openai"),
            embedding=EmbeddingConfig(provider="openai"),
            vector_store=VectorStoreConfig(provider="chroma"),
        )
        assert "openai" in repr(settings)
