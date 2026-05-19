from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Any, get_type_hints


@dataclass
class OpenAIConfig:
    model: str = ""
    api_key_env: str = ""


@dataclass
class AzureConfig:
    endpoint: str = ""
    api_key_env: str = ""
    api_version: str = ""
    deployment_name: str = ""


@dataclass
class OllamaConfig:
    base_url: str = "http://localhost:11434"
    model: str = ""


@dataclass
class DeepSeekConfig:
    model: str = ""
    api_key_env: str = ""


@dataclass
class LLMConfig:
    provider: str = ""
    openai: OpenAIConfig = field(default_factory=OpenAIConfig)
    azure: AzureConfig = field(default_factory=AzureConfig)
    ollama: OllamaConfig = field(default_factory=OllamaConfig)
    deepseek: DeepSeekConfig = field(default_factory=DeepSeekConfig)


@dataclass
class EmbeddingConfig:
    provider: str = ""
    openai: OpenAIConfig = field(default_factory=OpenAIConfig)
    azure: AzureConfig = field(default_factory=AzureConfig)
    ollama: OllamaConfig = field(default_factory=OllamaConfig)


@dataclass
class ChromaConfig:
    persist_directory: str = "data/db/chroma"


@dataclass
class VectorStoreConfig:
    provider: str = ""
    chroma: ChromaConfig = field(default_factory=ChromaConfig)


@dataclass
class DenseRetrievalConfig:
    top_k: int = 20


@dataclass
class SparseRetrievalConfig:
    top_k: int = 20


@dataclass
class FusionConfig:
    k: int = 60


@dataclass
class RetrievalConfig:
    final_top_k: int = 10
    dense: DenseRetrievalConfig = field(default_factory=DenseRetrievalConfig)
    sparse: SparseRetrievalConfig = field(default_factory=SparseRetrievalConfig)
    fusion: FusionConfig = field(default_factory=FusionConfig)


@dataclass
class RerankLLMConfig:
    prompt_path: str = ""


@dataclass
class CrossEncoderConfig:
    model: str = ""
    max_length: int = 512


@dataclass
class RerankConfig:
    backend: str = "none"
    llm: RerankLLMConfig = field(default_factory=RerankLLMConfig)
    cross_encoder: CrossEncoderConfig = field(default_factory=CrossEncoderConfig)


@dataclass
class ChunkRefinerConfig:
    use_llm: bool = False


@dataclass
class MetadataEnricherConfig:
    use_llm: bool = False


@dataclass
class IngestionConfig:
    chunk_size: int = 512
    chunk_overlap: int = 64
    batch_size: int = 10
    chunk_refiner: ChunkRefinerConfig = field(default_factory=ChunkRefinerConfig)
    metadata_enricher: MetadataEnricherConfig = field(default_factory=MetadataEnricherConfig)


@dataclass
class RagasConfig:
    metrics: list[str] = field(default_factory=list)


@dataclass
class EvaluationConfig:
    backends: list[str] = field(default_factory=list)
    ragas: RagasConfig = field(default_factory=RagasConfig)


@dataclass
class ObservabilityConfig:
    log_level: str = "INFO"
    trace_enabled: bool = True
    traces_path: str = "logs/traces.jsonl"
    app_log_path: str = "logs/app.log"


@dataclass
class Settings:
    llm: LLMConfig = field(default_factory=LLMConfig)
    embedding: EmbeddingConfig = field(default_factory=EmbeddingConfig)
    vector_store: VectorStoreConfig = field(default_factory=VectorStoreConfig)
    retrieval: RetrievalConfig = field(default_factory=RetrievalConfig)
    rerank: RerankConfig = field(default_factory=RerankConfig)
    ingestion: IngestionConfig = field(default_factory=IngestionConfig)
    evaluation: EvaluationConfig = field(default_factory=EvaluationConfig)
    observability: ObservabilityConfig = field(default_factory=ObservabilityConfig)


_REQUIRED_FIELDS = [
    ("llm.provider", "LLM provider is required"),
    ("embedding.provider", "Embedding provider is required"),
    ("vector_store.provider", "VectorStore provider is required"),
]


def _populate_dataclass(dc: Any, data: dict[str, Any]) -> None:
    hints = get_type_hints(type(dc))
    for f in fields(dc):
        if f.name in data:
            value = data[f.name]
            field_type = hints.get(f.name)
            if isinstance(value, dict) and field_type and _is_dataclass_type(field_type):
                nested = field_type()
                _populate_dataclass(nested, value)
                setattr(dc, f.name, nested)
            else:
                setattr(dc, f.name, value)


def _is_dataclass_type(tp: Any) -> bool:
    return hasattr(tp, "__dataclass_fields__")


def load_settings(path: str) -> Settings:
    import yaml
    import os

    if not os.path.isfile(path):
        raise FileNotFoundError(f"Settings file not found: {path}")

    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    if raw is None:
        raise ValueError(f"Settings file is empty: {path}")

    settings = Settings()
    _populate_dataclass(settings, raw)
    validate_settings(settings)
    return settings


def validate_settings(settings: Settings) -> None:
    missing: list[str] = []

    for field_path, error_msg in _REQUIRED_FIELDS:
        value = _get_nested_attr(settings, field_path)
        if not value:
            missing.append(f"{field_path}: {error_msg}")

    if missing:
        raise ValueError(
            "Settings validation failed - missing required fields:\n  "
            + "\n  ".join(missing)
        )


def _get_nested_attr(obj: Any, dotted_path: str) -> Any:
    parts = dotted_path.split(".")
    current = obj
    for part in parts:
        if hasattr(current, part):
            current = getattr(current, part)
        else:
            return None
    return current
