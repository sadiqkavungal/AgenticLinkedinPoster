from langchain_groq import ChatGroq
from langchain.llms.base import LLM
from config import Config

def get_llm() -> LLM:
    """
    Returns an instance of the ChatGroq LLM configured with the desired model.
    """
    # Expose Groq key as environment variable for the library to pick up
    # or optionally set it programmatically:
    import os
    os.environ["GROQ_API_KEY"] = Config.GROQ_API_KEY
    return ChatGroq(model=Config.LLM_MODEL_NAME)
