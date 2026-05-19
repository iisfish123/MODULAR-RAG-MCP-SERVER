import sys
import os


def main() -> None:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

    from observability.logger import get_logger
    from core.settings import load_settings

    logger = get_logger("main")

    try:
        settings_path = os.path.join(os.path.dirname(__file__), "config", "settings.yaml")
        settings = load_settings(settings_path)
        logger.info("Settings loaded successfully")
    except (FileNotFoundError, ValueError) as e:
        logger.error("Failed to load settings: %s", e)
        sys.exit(1)

    try:
        import mcp_server
        import core
        import ingestion
        import libs
        import observability
    except ImportError as e:
        logger.error("Failed to import key packages: %s", e)
        sys.exit(1)

    logger.info("Modular RAG MCP Server started successfully")
    logger.info("LLM provider: %s", settings.llm.provider)
    logger.info("Embedding provider: %s", settings.embedding.provider)
    logger.info("VectorStore provider: %s", settings.vector_store.provider)
    logger.info("Phase A: Engineering skeleton is ready.")


if __name__ == "__main__":
    main()
