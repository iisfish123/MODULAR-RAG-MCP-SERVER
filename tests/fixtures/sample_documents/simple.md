# Sample document for testing
# This file simulates a markdown document converted from PDF.

# Sample Technical Document

## Introduction

This is a sample technical document used for testing the ingestion pipeline.
It contains multiple sections, paragraphs, and formatting elements.

## Architecture Overview

The system follows a modular architecture with the following components:

1. Ingestion Pipeline
2. Retrieval Engine
3. MCP Server
4. Dashboard

## Configuration

To configure the system, edit the `config/settings.yaml` file.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| llm.provider | string | openai | The LLM provider to use |
| embedding.provider | string | openai | The embedding provider to use |
| vector_store.provider | string | chroma | The vector store backend |

## Code Example

```python
def main():
    settings = load_settings("config/settings.yaml")
    pipeline = IngestionPipeline(settings)
    pipeline.run("path/to/document.pdf")
```

## Conclusion

This document serves as a minimal test fixture for the ingestion pipeline.
