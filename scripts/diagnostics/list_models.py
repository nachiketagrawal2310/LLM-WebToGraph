import os
import logging
from huggingface_hub import HfApi


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    token = os.getenv("HUGGINGFACEHUB_API_TOKEN") or os.getenv("HF_TOKEN")
    search = os.getenv("HF_MODEL_SEARCH", "Qwen")
    limit = int(os.getenv("HF_MODEL_LIMIT", "25"))

    api = HfApi(token=token)

    try:
        logger.info("Listing Hugging Face models (search=%s, limit=%s)", search, limit)
        models = api.list_models(search=search, limit=limit, sort="downloads", direction=-1)
        for model in models:
            logger.info("Model: %s", model.id)
    except Exception as e:
        logger.exception("Error listing Hugging Face models: %s", e)


if __name__ == "__main__":
    main()
