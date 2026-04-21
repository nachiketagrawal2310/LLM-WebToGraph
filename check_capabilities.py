import os
import logging
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check():
    try:
        model_name = os.getenv("HF_MODEL_ID", "Qwen/Qwen3-30B-A3B-Instruct-2507")
        token = os.getenv("HUGGINGFACEHUB_API_TOKEN") or os.getenv("HF_TOKEN")
        llm = ChatHuggingFace(
            llm=HuggingFaceEndpoint(
                repo_id=model_name,
                task="text-generation",
                provider=os.getenv("HF_INFERENCE_PROVIDER", "auto"),
                max_new_tokens=256,
                do_sample=False,
                huggingfacehub_api_token=token,
            )
        )

        if hasattr(llm, 'with_structured_output'):
            logger.info("with_structured_output is AVAILABLE")
        else:
            logger.warning("with_structured_output is NOT available")
            
        # Also check imports
        try:
            from langchain_huggingface import ChatHuggingFace as _CH
            logger.info("langchain_huggingface IMPORTABLE")
        except ImportError:
            logger.error("langchain_huggingface NOT IMPORTABLE")
            
    except Exception as e:
        logger.exception("Capability check failed: %s", e)

if __name__ == "__main__":
    check()
